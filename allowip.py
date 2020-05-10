#!/usr/bin/python
import boto3 
import sys

# by Rafael Klock

ec2 = boto3.client('ec2')
security_group_id = 'sg-080ce2a7c35e04bca'

ip_allow = sys.argv[1]

retorno = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': '-1',
             'IpRanges': [
		{'CidrIp': ip_allow,
		 'Description': 'Allowed by PortKnock'
                }]
	    }
        ])


print retorno
