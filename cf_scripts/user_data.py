__author__ = '562474'

from troposphere import Base64, Join, Ref, GetAtt

def jenkins_userData(password,**kwargs):
        return Base64(Join('', [
        '#!/bin/bash\n',
        'service ufw stop\n',
        'apt-get update\n',
        'apt-get install python-pip -y\n',
        'pip install awscli\n',
        'wget -O ~/bitnami-jenkins-1.639-0-linux-x64-installer.run https://bitnami.com/redirect/to/83504/bitnami-jenkins-1.639-0-linux-x64-installer.run?bypassauth=false\n',
        'chmod 754 ~/bitnami-jenkins-1.639-0-linux-x64-installer.run\n',
        '~/bitnami-jenkins-1.639-0-linux-x64-installer.run --prefix /opt/jenkins --mode unattended --base_password ',password,'\n',

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
        'ansible-playbook -i "127.0.0.1" elk_stack.yml',
    ]))