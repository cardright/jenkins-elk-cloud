#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Generates Cloud Formation Script

Info on the python library used to generate the script
https://github.com/cloudtools/troposphere

"""

import os
import datetime

from troposphere import Ref, Tags, Template,Parameter,  Base64, FindInMap, GetAtt, Join, Output
from troposphere.ec2 import Instance, NetworkAcl, Route, \
    VPCGatewayAttachment, SubnetRouteTableAssociation, Subnet, RouteTable, \
    VPC, NetworkAclEntry, InternetGateway, SecurityGroupRule, SecurityGroup, SecurityGroupIngress, EIP,\
    EIPAssociation, NetworkInterfaceProperty, Volume,VolumeAttachment

from troposphere import constants

from troposphere.iam import Role, InstanceProfile

from troposphere import iam  # avoid conflict with awacs.aws.Policy, so iam.Policy

from awacs.aws import Allow, Statement, Principal, Policy
from awacs.sts import AssumeRole
# Actions
from awacs.cloudformation import CancelUpdateStack, CreateStack, ListStackResources, DescribeStackEvents,  UpdateStack
from awacs.ec2 import RunInstances,DescribeInstances,DescribeInstanceStatus,AuthorizeSecurityGroupIngress, StartInstances
# Script Helpers

import mappings
import user_data
import template_helpers

ref_stack_id = Ref('AWS::StackId')
ref_region = Ref('AWS::Region')
ref_stack_name = Ref('AWS::StackName')
quad_zero_ip = constants.QUAD_ZERO  # '0.0.0.0/0'

candidate_id= 'candidate-8578e887'
candidate_name= 'mkowalsky'

add_elk_instance = True

t = Template()
t.add_description("""\
Cloud Formation Template.  Template Created: """ + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


jenkins_instance_type_param = t.add_parameter(Parameter(
    'jenkinsServerParam',
    Type='String',
    Description='Jenkins Server EC2 HVM Instance type',
    Default='m3.medium',
    AllowedValues=[
        't2.micro', 't2.small', 't2.medium',
        'm3.medium', 'm3.large', 'm3.xlarge', 'm3.2xlarge',
        'c3.large', 'c3.xlarge', 'c3.2xlarge', 'c3.4xlarge', 'c3.8xlarge',
        'r3.large', 'r3.xlarge', 'r3.2xlarge', 'r3.4xlarge', 'r3.8xlarge',
        'i2.xlarge', 'i2.2xlarge', 'i2.4xlarge', 'i2.8xlarge',
        'hi1.4xlarge',
        'hs1.8xlarge',
        'cr1.8xlarge',
        'cc2.8xlarge',
        'cg1.4xlarge',
    ],
    ConstraintDescription='Must be a valid EC2 instance type.',
))


ssh_key_param = t.add_parameter(Parameter(
    'sshKeyParam',
    Type = 'String',
    Description= 'SSH KeyPair Name used to SSH into Instances',
    ConstraintDescription='Must Not be Empty',
    MinLength=3
))

ssh_ip_param = t.add_parameter(Parameter(
    'sshIPParam',
    Type="String",
    MinLength=9,
    MaxLength=18,
    Default=quad_zero_ip,
    AllowedPattern= "(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})/(\\d{1,2})",
    ConstraintDescription='Must be valid IP CIDR range in the form of x.x.x.x/x.'))

jenkins_password_param = t.add_parameter(Parameter(
    'jenkinsPWParam',
    Type='String',
    Description="Jenkins default 'user' Password",
    NoEcho=True,
    ConstraintDescription='Must be greater than 5 characters',
    MinLength=5))

# Ubuntu 14
t.add_mapping(mappings.ubuntu_14_AWSRegionArch2AMI[mappings.logicalName],
              mappings.ubuntu_14_AWSRegionArch2AMI[mappings.mapping])

# Instance Type to architecture type -> HVM64, PV64, etc
t.add_mapping(mappings.AWSInstanceType2Arch[mappings.logicalName],
              mappings.AWSInstanceType2Arch[mappings.mapping])


VPC = t.add_resource(
    VPC(
        'ElkVPC',
        CidrBlock='10.0.0.0/16',
        EnableDnsSupport=True,
        EnableDnsHostnames=True,
        Tags=Tags(
            Name='ELK VPC',
            Candidate=candidate_name)))

public_tools_subnet = t.add_resource(
    Subnet(
        'publicToolsSubnet1',
        CidrBlock='10.0.8.0/24',
        MapPublicIpOnLaunch=True,
        VpcId=Ref(VPC),
        Tags=Tags(Name="Public Tools Subnet",
                  Candidate=candidate_name)))

internetGateway = t.add_resource(
    InternetGateway(
        'InternetGateway',
        Tags=Tags(
            Candidate=candidate_name)))

gatewayAttachment = t.add_resource(
    VPCGatewayAttachment(
        'AttachGateway',
        VpcId=Ref(VPC),
        InternetGatewayId=Ref(internetGateway)))

routeTable = t.add_resource(
    RouteTable(
        'publicRouteTable',
        VpcId=Ref(VPC),
        Tags=Tags(
        Candidate=candidate_name)))

route = t.add_resource(
    Route(
        'Route',
        DependsOn='AttachGateway',
        GatewayId=Ref('InternetGateway'),
        DestinationCidrBlock=quad_zero_ip,
        RouteTableId=Ref(routeTable),
    ))


t.add_resource(
    SubnetRouteTableAssociation(
        'publicToolsSubnetRouteTableAssoc1',
        SubnetId=Ref(public_tools_subnet),
        RouteTableId=Ref(routeTable),
    ))

public_tools_sg = t.add_resource(
    SecurityGroup(
        title='publicToolsSG1',
        GroupDescription='Enable Access to Servers',
        VpcId=Ref(VPC),
        Tags=Tags(Name='Default Security Group'),
        SecurityGroupIngress=[
            SecurityGroupRule(              # SSH
                IpProtocol='tcp',
                FromPort='22',
                ToPort='22',
                CidrIp=Ref(ssh_ip_param)),
            SecurityGroupRule(              # Web Interface
                IpProtocol='tcp',
                FromPort='80',
                ToPort='80',
                CidrIp=quad_zero_ip),
            SecurityGroupRule(              # HTTPS Web Interface
                IpProtocol='tcp',
                FromPort='443',
                ToPort='443',
                CidrIp=quad_zero_ip),
            SecurityGroupRule(              # Web Interface Kibana
                IpProtocol='tcp',
                FromPort='5601',
                ToPort='5601',
                CidrIp=quad_zero_ip)
        ]
    ))

jenkinsRole = t.add_resource(Role(
    "jenkinsRole",
    AssumeRolePolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Action=[AssumeRole],
                Principal=Principal("Service", ["ec2.amazonaws.com"]))
            ]
        ),
    Path="/",
    Policies=[iam.Policy(PolicyName="JenkinsPolicies",
                         PolicyDocument=Policy(
                             Statement=[
                                 Statement(Effect=Allow,
                                           Action=[CancelUpdateStack,
                                                   CreateStack,
                                                   ListStackResources,
                                                   DescribeStackEvents,
                                                   UpdateStack],
                                           Resource=[Ref('AWS::StackId')],),
                                 Statement(Effect=Allow,
                                           Action=[StartInstances,
                                                   RunInstances,
                                                   DescribeInstances,
                                                   DescribeInstanceStatus,
                                                   AuthorizeSecurityGroupIngress],
                                           Resource=["*"])
                             ]
                         ))

    ],
    ),
)


cfninstanceprofile = t.add_resource(InstanceProfile(
    "jenkinsRoleProfile",
    Roles=[Ref(jenkinsRole)]
))



jenkins_ec2_instance = t.add_resource(Instance(
    "jenkinsInstance1",
    ImageId=FindInMap(mappings.ubuntu_14_AWSRegionArch2AMI[mappings.logicalName], ref_region,
                      FindInMap(mappings.AWSInstanceType2Arch[mappings.logicalName], Ref(jenkins_instance_type_param), 'Arch')),

    InstanceType = Ref(jenkins_instance_type_param),
    IamInstanceProfile= Ref(cfninstanceprofile),
    KeyName=Ref(ssh_key_param),
    UserData=user_data.jenkins_userData(Ref(jenkins_password_param),Ref('AWS::Region'),Ref('AWS::StackId')),
    NetworkInterfaces=[
        NetworkInterfaceProperty(
            GroupSet=[Ref(public_tools_sg)],
            AssociatePublicIpAddress='true',
            DeviceIndex='0',
            DeleteOnTermination='true',
            SubnetId=Ref(public_tools_subnet) )
    ],
    Tags=Tags(Name="Jenkins Server",
              CandidateName=candidate_name),
    DependsOn=internetGateway.title
))

if add_elk_instance:
    elk_instance1 = t.add_resource(Instance(
        "elkInstance1",
        ImageId=FindInMap(mappings.ubuntu_14_AWSRegionArch2AMI[mappings.logicalName], ref_region,
                          FindInMap(mappings.AWSInstanceType2Arch[mappings.logicalName], Ref(jenkins_instance_type_param), 'Arch')),

        InstanceType = Ref(jenkins_instance_type_param),
        KeyName=Ref(ssh_key_param),
        UserData=user_data.elk_userData(),
        NetworkInterfaces=[
            NetworkInterfaceProperty(
                GroupSet=[Ref(public_tools_sg)],
                AssociatePublicIpAddress='true',
                DeviceIndex='0',
                DeleteOnTermination='true',
                SubnetId=Ref(public_tools_subnet) )
        ],
        Tags=Tags(Name="ELK Server",
                  CandidateName=candidate_name),
        DependsOn=internetGateway.title
    ))




# Attaches volume to instance.
# Default Volume size 20GB
# Default Mount Point is /dev/xvdb
# template_helpers.create_and_attach_volume(t,"Volume1", jenkins_ec2_instance, Size="15")


t.add_output(
    [Output('JenkinsURL',
            Description='Jenkins   application URL',
            Value=Join('',
                       ['http://', GetAtt(jenkins_ec2_instance.title, 'PublicIp'), '/jenkins'])  # Would not validate against the aws cli

            ),
     ]
    )

if add_elk_instance:
    json_path = os.path.join('..','jenkins_ELK_cfn_vpc_template.json')
else:
    json_path = os.path.join('..','jenkins_cfn_vpc_template.json')
with open(json_path, 'w') as f:
    f.write(t.to_json(indent=2))
print ('DONE')

import subprocess # Validate with aws commandline tool
subprocess.call("aws cloudformation validate-template --profile rean --region us-east-1 --template-body file://{0}".format(json_path)) #--profile rean --region US-East-1)