# -*- coding: utf-8 -*-

import sys

from opinel.utils import manage_dictionary, printInfo, printError, printException

from AWSScout2 import __version__ as scout2_version
from AWSScout2.services.vpc import get_cidr_name, put_cidr_name



def postprocessing(aws_config, current_time, ruleset):

    update_metadata(aws_config)
    update_last_run(aws_config, current_time, ruleset)


def update_last_run(aws_config, current_time, ruleset):
    last_run = {}
    last_run['time'] = current_time.strftime("%Y-%m-%d %H:%M:%S%z")
    last_run['cmd'] = ' '.join(sys.argv)
    last_run['version'] = scout2_version
    last_run['ruleset_name'] = ruleset.name
    last_run['ruleset_about'] = ruleset.ruleset['about'] if 'about' in ruleset.ruleset else ''
    last_run['summary'] = {}
    for service in aws_config['services']:
        last_run['summary'][service] = {'checked_items': 0, 'flagged_items': 0, 'max_level': 'warning'}
        if aws_config['services'][service] == None:
            # Not supported yet
            continue
        elif 'findings' in aws_config['services'][service]:
            for finding in aws_config['services'][service]['findings']:
                last_run['summary'][service]['checked_items'] += aws_config['services'][service]['findings'][finding]['checked_items']
                last_run['summary'][service]['flagged_items'] += aws_config['services'][service]['findings'][finding]['flagged_items']
                if last_run['summary'][service]['max_level'] != 'danger':
                    last_run['summary'][service]['max_level'] = aws_config['services'][service]['findings'][finding]['level']
    aws_config['last_run'] = last_run



#
# Create dashboard metadata
#
def update_metadata(aws_config):
    # Security risks dropdown on a per-resource basis

    service_map = {}
    for service_group in aws_config['metadata']:
        for service in aws_config['metadata'][service_group]:
            if service not in aws_config['service_list']:
                continue
            if 'resources' not in aws_config['metadata'][service_group][service]:
                continue
            service_map[service] = service_group
    for s in aws_config['services']:
        if aws_config['services'][s] and 'violations' in aws_config['services'][s]:
            for v in aws_config['services'][s]['violations']:
                # Finding resource
                resource_path = aws_config['services'][s]['violations'][v]['display_path'] if 'display_path' in aws_config['services'][s]['violations'][v] else aws_config['services'][s]['violations'][v]['path']
                resource = resource_path.split('.')[-2]
                # h4ck...
                if resource == 'credential_report':
                    resource = resource_path.split('.')[-1].replace('>', '').replace('<', '')
                elif resource == s:
                    resource = resource_path.split('.')[-1]
                if aws_config['services'][s]['violations'][v]['flagged_items'] > 0:
                    try:
                        manage_dictionary(aws_config['metadata'][service_map[s]][s]['resources'][resource], 'risks', [])
                        aws_config['metadata'][service_map[s]][s]['resources'][resource]['risks'].append(v)
                    except Exception as e:
                        try:
                            manage_dictionary(aws_config['metadata'][service_map[s]][s]['summaries'][resource], 'risks', [])
                            aws_config['metadata'][service_map[s]][s]['summaries'][resource]['risks'].append(v)
                        except Exception as e:
                            printError('Service: %s' % s)
                            printError('Resource: %s' % resource)
                            printException(e)




########################################
# VPC
########################################

def vpc_postprocessing(aws_config, ip_ranges = [], ip_ranges_name_key = None):

    # Add friendly name for CIDRs
    if len(ip_ranges):
        callback_args = {'ip_ranges': ip_ranges, 'ip_ranges_name_key': ip_ranges_name_key}
        go_to_and_do(aws_config, aws_config['services']['ec2'], ['regions', 'vpcs', 'security_groups', 'rules', 'protocols', 'ports'], ['services', 'ec2'], put_cidr_name, callback_args)

    # Propagate VPC names outside EC2
    vpc_services = [ 'rds', 'redshift' ]
#    for service in vpc_services:
#        go_to_and_do(aws_config, aws_config['services'][service], ['regions', 'vpcs'], ['services', service], propagate_vpc_names, {})



