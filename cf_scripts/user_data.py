__author__ = '562474'

from troposphere import Base64, Join, Ref, GetAtt

def jenkins_userData(password,region, stack_name,**kwargs):
        return Base64(Join('', [
        '#!/bin/bash\n',
        'service ufw stop\n',
        'apt-get update\n',
        'apt-get install python-pip -y\n',
        'pip install awscli\n',
        'wget -O ~/bitnami-jenkins-1.639-0-linux-x64-installer.run https://bitnami.com/redirect/to/83504/bitnami-jenkins-1.639-0-linux-x64-installer.run?bypassauth=false\n',
        'chmod 754 ~/bitnami-jenkins-1.639-0-linux-x64-installer.run\n',
        '~/bitnami-jenkins-1.639-0-linux-x64-installer.run --prefix /opt/jenkins --mode unattended --base_password ',password,'\n',
        'wget -O /tmp/jenkins_elk.json https://raw.githubusercontent.com/mkowalsky/jenkins-elk-cloud/master/jenkins_ELK_cfn_vpc_template.json\n',
        'wget -O /opt/update-stack.sh https://raw.githubusercontent.com/mkowalsky/jenkins-elk-cloud/master/update-stack.sh\n',
        'chmod 754 /opt/update-stack.sh\n',
        'wget -O /tmp/jenkinsJob.xml https://raw.githubusercontent.com/mkowalsky/jenkins-elk-cloud/master/jenkinsJob.xml\n',
        'curl -u user:', password,' -X POST -H "Content-Type:application/xml" -d @/tmp/jenkinsJob.xml "http://localhost/jenkins/createItem?name=DeployELK" \n'
        'curl -u user:',password,' -X POST http://localhost/jenkins/job/DeployELK/buildWithParameters?stack_name=',stack_name,'&input_file=/tmp/jenkins_elk.json&stack_region=',region,'\n',
    ]))

def elk_userData(**kwargs):
        return Base64(Join('', [
        '#!/bin/bash\n',
        'service ufw stop\n',
        'apt-get update\n',
        'apt-get python-pycurl -y\n',
        'apt-get install software-properties-common -y\n',
        'apt-add-repository ppa:ansible/ansible\n',
        'apt-get update\n',
        'apt-get install ansible -y\n',
        'wget https://raw.githubusercontent.com/mkowalsky/jenkins-elk-cloud/master/cm_tool/elk_stack.yml\n',
        'ansible-playbook -i "127.0.0.1," elk_stack.yml',
    ]))