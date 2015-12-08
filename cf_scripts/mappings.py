#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Contains Mapping values for Servers in VPC

Info on the python library used to generate the script
https://github.com/cloudtools/troposphere

"""

from troposphere import constants

logicalName = 'logicalName'
mapping = 'mapping'

PV64 = 'PV64'
HVM64 = 'HVM64'
HVMG2 = 'HVMG2' # GPU Instance

PV64_MAP =  {'Arch': PV64}
HVM64_MAP = {'Arch': HVM64}
HVMG2_MAP = {'Arch': HVMG2} # GPU Instance

AWSInstanceType2Arch = {
    logicalName :'AWSInstanceType2Arch',
    mapping : {
        't1.micro':  PV64_MAP,

        't2.micro':  HVM64_MAP,
        't2.small':  HVM64_MAP,
        't2.medium': HVM64_MAP,

        'm1.small':  PV64_MAP,
        'm1.medium': PV64_MAP,
        'm1.large':  PV64_MAP,
        'm1.xlarge': PV64_MAP,
        'm2.xlarge': PV64_MAP,
        'm2.2xlarge': PV64_MAP,
        'm2.4xlarge': PV64_MAP,

        'm3.medium':  HVM64_MAP,
        'm3.large':   HVM64_MAP,
        'm3.xlarge':  HVM64_MAP,
        'm3.2xlarge': HVM64_MAP,

        'c1.medium':  PV64_MAP,
        'c1.xlarge':  PV64_MAP,

        'c3.large':   HVM64_MAP,
        'c3.xlarge':  HVM64_MAP,
        'c3.2xlarge': HVM64_MAP,
        'c3.4xlarge': HVM64_MAP,
        'c3.8xlarge': HVM64_MAP,
        'g2.2xlarge': HVMG2_MAP,

        'r3.large':   HVM64_MAP,
        'r3.xlarge':  HVM64_MAP,
        'r3.2xlarge': HVM64_MAP,
        'r3.4xlarge': HVM64_MAP,
        'r3.8xlarge': HVM64_MAP,

        'i2.xlarge':  HVM64_MAP,
        'i2.2xlarge': HVM64_MAP,
        'i2.4xlarge': HVM64_MAP,
        'i2.8xlarge': HVM64_MAP,

        'hi1.4xlarge': HVM64_MAP,
        'hs1.8xlarge': HVM64_MAP,
        'cr1.8xlarge': HVM64_MAP,
        'cc2.8xlarge': HVM64_MAP,
    }}


centos_7_AWSRegionArch2AMI = {
    logicalName: 'centos7AWSRegionArch2AMI',
    mapping: {
        constants.US_EAST_1: {HVM64: "ami-96a818fe"},
        constants.US_WEST_1: {HVM64: "ami-6bcfc42e"},
        constants.US_WEST_2: {HVM64: "ami-c7d092f7"}

    }}

"""
 Ambari Server and Hadoop Cluster Images
 OS: CentOS 6 (x86_64) - with Updates HVM
 AWS: https://aws.amazon.com/marketplace/pp/B00NQAYLWO

 CentOS 6 x86_64 (2014_09_29) EBS HVM
 CentOS 6 x86_64 (2014_09_29) EBS HVM-74e73035-3435-48d6-88e0-89cc02ad83ee-ami-a8a117c0.2
"""
centos_65_AWSRegionArch2AMI = {
    logicalName: 'centos65AWSRegionArch2AMI',
    mapping : {
        constants.US_EAST_1: {HVM64: 'ami-c2a818aa'},    # market place image
        constants.US_WEST_1: {HVM64: 'ami-57cfc412'},    # market place image
        constants.US_WEST_2: {HVM64: 'ami-81d092b1'}     # market place image
    }}

"""
 Ubuntu 14.04 Trusty 64 hvm-ssd instances
 ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-20150325

 http://cloud-images.ubuntu.com/locator/

"""
ubuntu_14_AWSRegionArch2AMI = {
    logicalName: 'ubuntu14AWSRegionArch2AMI',
    mapping : {
        constants.US_EAST_1: {HVM64: 'ami-d05e75b8'},
        constants.US_WEST_1: {HVM64: 'ami-df6a8b9b'},
        constants.US_WEST_2: {HVM64: 'ami-5189a661'},
        constants.AP_NORTHEAST_1: {HVM64: 'ami-936d9d93'},
        constants.AP_SOUTHEAST_1: {HVM64: 'ami-96f1c1c4'},
        constants.AP_SOUTHEAST_2: {HVM64: 'ami-69631053'},
        constants.EU_CENTRAL_1: {HVM64: 'ami-accff2b1'},
        constants.EU_WEST_1: {HVM64:'ami-47a23a30' },
        constants.SA_EAST_1: {HVM64: 'ami-4d883350'}
    }}

"""
 Ubuntu Server 12.04 LTS (HVM)
 ubuntu/images/hvm-ssd/ubuntu-precise-12.04-amd64-server-20150127-f4f523b3-d6b3-42a4-82e8-5f264cf4cf91-ami-f2bbff9a.2

http://cloud-images.ubuntu.com/locator/
"""
ubuntu_12_AWSRegionArch2AMI = {
    logicalName: 'ubuntu12AWSRegionArch2AMI',
    mapping : {
        constants.US_EAST_1: {HVM64: 'ami-427a392a'},
        constants.US_WEST_1: {HVM64: 'ami-82bba3c7'},
        constants.US_WEST_2: {HVM64: 'ami-2b471c1b'}
    }}

"""
aws ec2 describe-images --region us-xxxx-n --filter "Name=name,Values=amzn-ami-vpc-nat-hvm-2015*"
-query Images[*].{Name:Name,Arch:Architecture,Description:Description,Id:ImageId,CreationDate:CreationDate,RootVolumeType:RootDeviceType}

Amazon Linux AMI VPC NAT x86_64 HVM
amzn-ami-vpc-nat-hvm-2015.03.0.x86_64-ebs
"""

ami_nat_instanceAWSRegionArch2AMI = {
    logicalName: 'amazonNATInstance',
    mapping :{
            constants.US_EAST_1: {HVM64: 'ami-b0210ed8'},
            constants.US_WEST_1: {HVM64: 'ami-ada746e9'},
            constants.US_WEST_2: {HVM64: 'ami-75ae8245'}
    }}

"""
Instance Mapping Template

AWSRegionArch2AMI = {
    logicalName: 'AWSRegionArch2AMI',
    mapping : {
        'us-east-1': { 'PV64': None,
                      'HVM64': None,
                      'HVMG2': None'},
        'us-west-2': {'PV64': None,
                      'HVM64': None,
                      'HVMG2': None},
        'us-west-1': {'PV64': None,
                      'HVM64': None,
                      'HVMG2': None},
        # 'eu-west-1': {'PV64': 'ami-aa8f28dd',
        #               'HVM64': 'ami-748e2903',
        #               'HVMG2': 'ami-00913777'},
        # 'ap-southeast-1': {'PV64': 'ami-20e1c572',
        #                    'HVM64': 'ami-d6e1c584',
        #                    'HVMG2': 'ami-fabe9aa8'},
        # 'ap-northeast-1': {'PV64': 'ami-21072820',
        #                    'HVM64': 'ami-35072834',
        #                    'HVMG2': 'ami-5dd1ff5c'},
        # 'ap-southeast-2': {'PV64': 'ami-8b4724b1',
        #                    'HVM64': 'ami-fd4724c7',
        #                    'HVMG2': 'ami-e98ae9d3'},
        # 'sa-east-1': {'PV64': 'ami-9d6cc680',
        #               'HVM64': 'ami-956cc688',
        #               'HVMG2': 'NOT_SUPPORTED'},
        # 'cn-north-1': {'PV64': 'ami-a857c591',
        #                'HVM64': 'ami-ac57c595',
        #                'HVMG2': 'NOT_SUPPORTED'},
        # 'eu-central-1': {'PV64': 'ami-a03503bd',
        #                  'HVM64': 'ami-b43503a9',
        #                  'HVMG2': 'ami-b03503ad'},
    }}

"""