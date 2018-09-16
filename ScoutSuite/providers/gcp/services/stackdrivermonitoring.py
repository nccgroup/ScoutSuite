# -*- coding: utf-8 -*-

from opinel.utils.console import printError

from ScoutSuite.providers.gcp.configs.base import GCPBaseConfig


class StackdriverMonitoringConfig(GCPBaseConfig):
    targets = (
        # ('resources', 'Resources', 'list_monitored_resource_descriptors', {'name': 'project_placeholder'}, False),
    )

    def __init__(self, thread_config):
        self.library_type = 'cloud_client_library'

        self.resources = {}
        self.resources_count = 0

        super(StackdriverMonitoringConfig, self).__init__(thread_config)

    def parse_resources(self, resource, params):
        a = 1
