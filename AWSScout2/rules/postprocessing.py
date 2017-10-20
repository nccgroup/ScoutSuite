# -*- coding: utf-8 -*-

import sys

from opinel.utils.console import printException

from AWSScout2 import __version__ as scout2_version



def postprocessing(aws_config, current_time, ruleset):
    """

    :param aws_config:
    :param current_time:
    :param ruleset:
    :return:
    """
    update_metadata(aws_config)
    update_last_run(aws_config, current_time, ruleset)


def update_last_run(aws_config, current_time, ruleset):
    last_run = {}
    last_run['time'] = current_time.strftime("%Y-%m-%d %H:%M:%S%z")
    last_run['cmd'] = ' '.join(sys.argv)
    last_run['version'] = scout2_version
    last_run['ruleset_name'] = ruleset.name
    last_run['ruleset_about'] = ruleset.about
    last_run['summary'] = {}
    for service in aws_config['services']:
        last_run['summary'][service] = {'checked_items': 0, 'flagged_items': 0, 'max_level': 'warning', 'rules_count': 0, 'resources_count': 0}
        if aws_config['services'][service] == None:
            # Not supported yet
            continue
        elif 'findings' in aws_config['services'][service]:
            for finding in aws_config['services'][service]['findings'].values():
                last_run['summary'][service]['rules_count'] += 1
                last_run['summary'][service]['checked_items'] += finding['checked_items']
                last_run['summary'][service]['flagged_items'] += finding['flagged_items']
                items = finding.get('items', [])
                if last_run['summary'][service]['max_level'] != 'danger' and len(items) > 0:
                    last_run['summary'][service]['max_level'] = finding['level']
        # Total number of resources
        for key in aws_config['services'][service]:
            if key != 'regions_count' and key.endswith('_count'):
                last_run['summary'][service]['resources_count'] += aws_config['services'][service][key]
    aws_config['last_run'] = last_run


def update_metadata(aws_config):
        service_map = {}
        for service_group in aws_config['metadata']:
            for service in aws_config['metadata'][service_group]:
                if service not in aws_config['service_list']:
                    continue
                if 'hidden' in aws_config['metadata'][service_group][service] and aws_config['metadata'][service_group][service]['hidden'] == True:
                    continue
                if 'resources' not in aws_config['metadata'][service_group][service]:
                    continue
                service_map[service] = service_group
                for resource in aws_config['metadata'][service_group][service]['resources']:
                    # full_path = path if needed
                    if not 'full_path' in aws_config['metadata'][service_group][service]['resources'][resource]:
                        aws_config['metadata'][service_group][service]['resources'][resource]['full_path'] = aws_config['metadata'][service_group][service]['resources'][resource]['path']
                    # Script is the full path minus "id" (TODO: change that)
                    if not 'script' in aws_config['metadata'][service_group][service]['resources'][resource]:
                        aws_config['metadata'][service_group][service]['resources'][resource]['script'] = '.'.join([x for x in aws_config['metadata'][service_group][service]['resources'][resource]['full_path'].split('.') if x != 'id'])
                    # Update counts
                    count = '%s_count' % resource
                    service_config = aws_config['services'][service]
                    if service_config and resource != 'regions':
                      if 'regions' in service_config.keys(): # hasattr(service_config, 'regions'):
                        aws_config['metadata'][service_group][service]['resources'][resource]['count'] = 0
                        for region in service_config['regions']:
                            if count in service_config['regions'][region].keys():
                                aws_config['metadata'][service_group][service]['resources'][resource]['count'] += service_config['regions'][region][count]
                      else:
                          try:
                            aws_config['metadata'][service_group][service]['resources'][resource]['count'] = service_config[count]
                          except Exception as e:

                              printException(e)
