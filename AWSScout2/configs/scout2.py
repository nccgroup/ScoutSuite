# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import json
import os

from opinel.utils.console import printException

from AWSScout2.configs.services import ServicesConfig

class Scout2Config(object):
    """
    Root object that holds all of the necessary AWS resources and Scout2
    configuration items.

    :aws_account_id     AWS account ID
    :last_run           Information about the last run
    :metadata           Metadata used to generate the HTML report
    :ruleset            Ruleset used to perform the analysis
    :services           AWS configuration sorted by service
    """

    def __init__(self, profile, report_dir = None, timestamp = None, services= [], skipped_services = [], thread_config = 4):
        self.aws_account_id = None
        self.last_run = None
        self.__load_metadata()
        self.services = ServicesConfig(self.metadata, thread_config)
        supported_services = vars(self.services).keys()
        self.service_list = self.__build_services_list(supported_services, services, skipped_services)


    def fetch(self, credentials, regions = [], skipped_regions = [], partition_name = 'aws'):
        """

        :param credentials:
        :param services:
        :param skipped_services:
        :param regions:
        :param skipped_regions:
        :param partition_name:
        :return:
        """
        # TODO: determine partition name based on regions and warn if multiple partitions...
        self.services.fetch(credentials, self.service_list, regions, partition_name)


    def __load_metadata(self):
        # Load metadata
        scout2_configs_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
        with open(os.path.join(scout2_configs_data_path, 'metadata.json'), 'rt') as f:
            self.metadata = json.load(f)


    def __build_services_list(self, supported_services, services, skipped_services):
        return [s for s in supported_services if (services == [] or s in services) and s not in skipped_services]


    def update_metadata(self):
        service_map = {}
        for service_group in self.metadata:
            for service in self.metadata[service_group]:
                if service not in self.service_list:
                    continue
                if 'resources' not in self.metadata[service_group][service]:
                    continue
                service_map[service] = service_group
                for resource in self.metadata[service_group][service]['resources']:
                    # full_path = path if needed
                    if not 'full_path' in self.metadata[service_group][service]['resources'][resource]:
                        self.metadata[service_group][service]['resources'][resource]['full_path'] = self.metadata[service_group][service]['resources'][resource]['path']
                    # Script is the full path minus "id" (TODO: change that)
                    if not 'script' in self.metadata[service_group][service]['resources'][resource]:
                        self.metadata[service_group][service]['resources'][resource]['script'] = '.'.join([x for x in self.metadata[service_group][service]['resources'][resource]['full_path'].split('.') if x != 'id'])
                    # Update counts
                    count = '%s_count' % resource
                    service_config = getattr(self.services, service)
                    if service_config and resource != 'regions':
                      if hasattr(service_config, 'regions'):
                        self.metadata[service_group][service]['resources'][resource]['count'] = 0
                        for region in service_config.regions:
                            if hasattr(service_config.regions[region], count):
                                self.metadata[service_group][service]['resources'][resource]['count'] += getattr(service_config.regions[region], count)
                      else:
                          try:
                              self.metadata[service_group][service]['resources'][resource]['count'] = getattr(service_config, count)
                          except Exception as e:
                              printException(e)
                              print(vars(service_config))
