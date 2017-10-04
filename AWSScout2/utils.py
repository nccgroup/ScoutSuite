# -*- coding: utf-8 -*-
from __future__ import print_function

import re



########################################
# Globals
########################################

ec2_classic = 'EC2-Classic'

formatted_service_name = {
    'cloudformation': 'CloudFormation',
    'cloudtrail': 'CloudTrail',
    'cloudwatch': 'CloudWatch',
    'directconnect': 'Direct Connect',
    'elasticache': 'ElastiCache',
    'lambda': 'Lambda',
    'redshift': 'RedShift',
    'route53': 'Route53',
    'route53domains': 'Route53Domains'
}


########################################
# Functions
########################################

def format_service_name(service):
    """

    :param service:
    :return:
    """
    return formatted_service_name[service] if service in formatted_service_name else service.upper()


def get_keys(src, dst, keys):
    """
    Copies the value of keys from source object to dest object

    :param src:
    :param dst:
    :param keys:
    :return:
    """
    for key in keys:
        #dst[no_camel(key)] = src[key] if key in src else None
        dst[key] = src[key] if key in src else None


def no_camel(name):
    """
    Converts CamelCase to camel_case

    :param name:
    :return:
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def is_throttled(e):
    """
    Determines whether the exception is due to API throttling.

    :param e:                           Exception raised
    :return:                            True if it's a throttling exception else False
    """
    return True if  (hasattr(e, 'response') and 'Error' in e.response and e.response['Error']['Code'] in [ 'Throttling', 'RequestLimitExceeded', 'ThrottlingException' ]) else False
