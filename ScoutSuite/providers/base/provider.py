# -*- coding: utf-8 -*-

import sys

from opinel.utils.console import printException

from ScoutSuite import __version__ as scout2_version


class BaseProvider:
    """
    Base class for the different providers.
    For each supported cloud provider, a child class will be created which implements the necessary code.
    In addition, each method of children classes will call the base provider in order to execute code required for
    all cloud providers
    """

    def __init__(self, config):
        self.config = config

    def preprocessing(self, ip_ranges=[], ip_ranges_name_key=None):
        """
        TODO

        :return: None
        """
        pass

    def postprocessing(self, current_time, ruleset):
        """
        TODO

        :param config:
        :param current_time:
        :param ruleset:
        :return: None
        """
        self.update_metadata(self.config)
        self.update_last_run(self.config, current_time, ruleset)

    def _asdf(self):
        pass

    def update_last_run(self, current_time, ruleset):
        last_run = {}
        last_run['time'] = current_time.strftime("%Y-%m-%d %H:%M:%S%z")
        last_run['cmd'] = ' '.join(sys.argv)
        last_run['version'] = scout2_version
        last_run['ruleset_name'] = ruleset.name
        last_run['ruleset_about'] = ruleset.about
        last_run['summary'] = {}
        for service in self.config['services']:
            last_run['summary'][service] = {'checked_items': 0, 'flagged_items': 0, 'max_level': 'warning',
                                            'rules_count': 0, 'resources_count': 0}
            if self.config['services'][service] == None:
                # Not supported yet
                continue
            elif 'findings' in self.config['services'][service]:
                for finding in self.config['services'][service]['findings'].values():
                    last_run['summary'][service]['rules_count'] += 1
                    last_run['summary'][service]['checked_items'] += finding['checked_items']
                    last_run['summary'][service]['flagged_items'] += finding['flagged_items']
                    items = finding.get('items', [])
                    if last_run['summary'][service]['max_level'] != 'danger' and len(items) > 0:
                        last_run['summary'][service]['max_level'] = finding['level']
            # Total number of resources
            for key in self.config['services'][service]:
                if key != 'regions_count' and key.endswith('_count'):
                    last_run['summary'][service]['resources_count'] += self.config['services'][service][key]
        self.config['last_run'] = last_run

    def update_metadata(self, config):
        service_map = {}
        for service_group in self.config['metadata']:
            for service in self.config['metadata'][service_group]:
                if service not in self.config['service_list']:
                    continue
                if 'hidden' in self.config['metadata'][service_group][service] and \
                        self.config['metadata'][service_group][service]['hidden'] == True:
                    continue
                if 'resources' not in self.config['metadata'][service_group][service]:
                    continue
                service_map[service] = service_group
                for resource in self.config['metadata'][service_group][service]['resources']:
                    # full_path = path if needed
                    if not 'full_path' in self.config['metadata'][service_group][service]['resources'][resource]:
                        self.config['metadata'][service_group][service]['resources'][resource]['full_path'] = \
                            self.config['metadata'][service_group][service]['resources'][resource]['path']
                    # Script is the full path minus "id" (TODO: change that)
                    if not 'script' in self.config['metadata'][service_group][service]['resources'][resource]:
                        self.config['metadata'][service_group][service]['resources'][resource]['script'] = '.'.join(
                            [x for x in
                             self.config['metadata'][service_group][service]['resources'][resource]['full_path'].split(
                                 '.') if x != 'id'])
                    # Update counts
                    count = '%s_count' % resource
                    service_config = self.config['services'][service]
                    if service_config and resource != 'regions':
                        if 'regions' in service_config.keys():  # hasattr(service_config, 'regions'):
                            self.config['metadata'][service_group][service]['resources'][resource]['count'] = 0
                            for region in service_config['regions']:
                                if count in service_config['regions'][region].keys():
                                    self.config['metadata'][service_group][service]['resources'][resource]['count'] += \
                                        service_config['regions'][region][count]
                        else:
                            try:
                                self.config['metadata'][service_group][service]['resources'][resource]['count'] = \
                                    service_config[count]
                            except Exception as e:

                                printException(e)
