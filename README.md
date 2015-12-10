# jenkins-elk-cloud
Simple repository using Cloudformation to deploy Jenkins and ELK Stack

## Objective:

Use CM tools such as Puppet, Ansible (preferable), or Chef to automate the installation of ElasticSearch, Logstash and Kibana(ELK). This script must be triggered Jenkins job to set up ELK.
 
## Deliverable:

A Cloudformation template that launches a Jenkins AMI prepackaged with the job. When the job is run, it should automatically trigger the launch of an EC2 instance and install ELK.

## Configuration: 

Create an AWS VPC with Cloudformation Template with  publicly accessible subnet and the appropriate Security Group. 

## How to Run 
Execute the Cloudformation script called  "jenkins_cfn_vpc_template.json"

