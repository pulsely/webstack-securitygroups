import boto3
from botocore.exceptions import ClientError

import pprint

from django.conf import settings

def add_security_group_with_ip_to_security_group( security_group, ip_address, port, ip_protocol ):
    try:
        if hasattr(settings, 'AWS_SECURITY_GROUP_KEY_ID') and settings.AWS_SECURITY_GROUP_KEY_ID and \
                hasattr(settings, 'AWS_SECURITY_GROUP_ACCESS_KEY') and settings.AWS_SECURITY_GROUP_ACCESS_KEY:
            print(settings.AWS_SECURITY_GROUP_KEY_ID  )
            ec2 = boto3.client('ec2', aws_access_key_id=settings.AWS_SECURITY_GROUP_KEY_ID,
                               aws_secret_access_key=settings.AWS_SECURITY_GROUP_ACCESS_KEY, region_name=settings.AWS_REGION_SECURITY_GROUP)
        else:
            ec2 = boto3.client('ec2', region_name=settings.AWS_REGION_SECURITY_GROUP)


        data = ec2.authorize_security_group_ingress(
            GroupId=security_group,
            IpPermissions=[
                {'IpProtocol': ip_protocol,
                 'FromPort': port,
                 'ToPort': port,
                 'IpRanges': [{'CidrIp': '%s' % ip_address }]},
            ])
        flag_success = True
        error = None
    except ClientError as e:
        print(e)
        error = e
        flag_success = False

    return { 'flag_success' : flag_success, 'error' : error }

def describe_security_group( the_security_group ):
    response = None
    if hasattr(settings, 'AWS_SECURITY_GROUP_KEY_ID') and settings.AWS_SECURITY_GROUP_KEY_ID and \
            hasattr(settings, 'AWS_SECURITY_GROUP_ACCESS_KEY') and settings.AWS_SECURITY_GROUP_ACCESS_KEY:

        ec2 = boto3.client('ec2', aws_access_key_id=settings.AWS_SECURITY_GROUP_KEY_ID,
                           aws_secret_access_key=settings.AWS_SECURITY_GROUP_ACCESS_KEY, region_name=settings.AWS_REGION_SECURITY_GROUP)
    else:
        ec2 = boto3.client('ec2', region_name=settings.AWS_REGION_SECURITY_GROUP)

    try:
        response = ec2.describe_security_groups( GroupIds=[the_security_group,]) # tokyo

        if settings.DEBUG:
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(response)

        error = None

    except ClientError as e:
        if settings.DEBUG:
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(e)
        error = e

    return { 'response' : response, 'error' : error }
