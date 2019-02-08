# -*- coding: utf-8 -*-

from opinel.utils.console import printError

from ScoutSuite.providers.gcp.configs.base import GCPBaseConfig


class StackdriverLoggingConfig(GCPBaseConfig):
    targets = (
        ('sinks', 'Sinks', 'list_sinks', {'project': '{{project_placeholder}}'}, False),
    )

    def __init__(self, thread_config):
        self.library_type = 'cloud_client_library'

        self.sinks = {}
        self.sinks_count = 0

        super(StackdriverLoggingConfig, self).__init__(thread_config)

    def parse_sinks(self, sink, params):

        sink_dict = {}
        sink_dict['name'] = sink.name
        sink_dict['filter'] = sink.filter_
        sink_dict['destination'] = sink.destination

        self.sinks[sink_dict['name']] = sink_dict
