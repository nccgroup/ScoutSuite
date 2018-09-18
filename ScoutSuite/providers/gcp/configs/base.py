# -*- coding: utf-8 -*-

# Python2 vs Python3
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from ScoutSuite.providers.base.configs.base import BaseConfig


class GCPBaseConfig(BaseConfig):

    def __init__(self, thread_config=4, projects=[], **kwargs):

        self.library_type = None if not self.library_type else self.library_type

        self.projects = projects

        super(GCPBaseConfig, self).__init__(thread_config)

    def _is_provider(self, provider_name):
        if provider_name == 'gcp':
            return True
        else:
            return False

    def get_zones(self, **kwargs):
        """
        Certain services require to be poled per-zone. In these cases, this method will return a list of zones to poll
        or None.

        :return:
        """
        return None
