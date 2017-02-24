# -*- coding: utf-8 -*-
"""
Foobar
"""

formatted_service_name = {
    'cloudtrail': 'CloudTrail',
    'cloudwatch': 'CloudWatch',
    'lambda': 'Lambda',
    'redshift': 'RedShift',
    'route53': 'Route53'
}

def format_service_name(service):
    """

    :param service:
    :return:
    """
    return formatted_service_name[service] if service in formatted_service_name else service.upper()


