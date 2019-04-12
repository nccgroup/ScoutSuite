import re
import time
from collections import Counter

import boto3
from botocore.session import Session

from ScoutSuite.core.console import print_exception, print_info

ec2_classic = 'EC2-Classic'


def connect_service(service, credentials, region_name=None, config=None, silent=False):
    """
    Instantiates an AWS API client

    :param service:                     Service targeted, e.g. ec2
    :param credentials:                 Id, secret, token
    :param region_name:                 Region desired, e.g. us-east-2
    :param config:                      Configuration (optional)
    :param silent:                      Whether or not to print messages

    :return:
    """
    api_client = None
    try:
        client_params = {'service_name': service.lower()}
        session_params = {'aws_access_key_id': credentials.get('access_key'),
                          'aws_secret_access_key': credentials.get('secret_key'),
                          'aws_session_token': credentials.get('token')}
        if region_name:
            client_params['region_name'] = region_name
            session_params['region_name'] = region_name
        if config:
            client_params['config'] = config
        aws_session = boto3.session.Session(**session_params)
        if not silent:
            info_message = 'Connecting to AWS %s' % service
            if region_name:
                info_message = info_message + ' in %s' % region_name
            print_info('%s...' % info_message)
        api_client = aws_session.client(**client_params)
    except Exception as e:
        print_exception(e)
    return api_client


def get_keys(src, dst, keys):
    """
    Copies the value of keys from source object to dest object

    :param src:                         Source object
    :param dst:                         Destination object
    :param keys:                        Keys
    :return:
    """
    for key in keys:
        dst[key] = src[key] if key in src else None


def get_name(src, dst, default_attribute):
    """

    :param src:                         Source object
    :param dst:                         Destination object
    :param default_attribute:           Default attribute

    :return:
    """
    name_found = False
    if 'Tags' in src:
        for tag in src['Tags']:
            if tag['Key'] == 'Name' and tag['Value'] != '':
                dst['name'] = tag['Value']
                name_found = True
    if not name_found:
        dst['name'] = src[default_attribute]
    return dst['name']


def get_caller_identity(credentials):
    api_client = connect_service('sts', credentials, silent=True)
    return api_client.get_caller_identity()


def get_aws_account_id(credentials):
    caller_identity = get_caller_identity(credentials)
    return caller_identity['Arn'].split(':')[4]


def get_partition_name(credentials):
    caller_identity = get_caller_identity(credentials)
    return caller_identity['Arn'].split(':')[1]

def is_throttled(e):
    """
    Determines whether the exception is due to API throttling.

    :param e:                           Exception raised
    :return:                            True if it's a throttling exception else False
    """
    return (hasattr(e, 'response') and 'Error' in e.response
            and e.response['Error']['Code'] in ['Throttling',
                                                'RequestLimitExceeded',
                                                'ThrottlingException'])


def no_camel(name):
    """
    Converts CamelCase to camel_case

    :param name:                        Name string to convert
    :return:
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
