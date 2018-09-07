# -*- coding: utf-8 -*-

# Python2 vs Python3
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from ScoutSuite.providers.base.configs.base import BaseConfig


class GCPBaseConfig(BaseConfig):

    def __init__(self, thread_config):

        self.library_type = None

        super(GCPBaseConfig, self).__init__(thread_config)



    def _is_provider(self, provider_name):
        if provider_name == 'gcp':
            return True
        else:
            return False
