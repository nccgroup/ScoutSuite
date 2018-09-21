# -*- coding: utf-8 -*-

# Python2 vs Python3
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from ScoutSuite.providers.base.configs.base import BaseConfig


class AzureBaseConfig(BaseConfig):

    def __init__(self, thread_config=4, **kwargs):

        super(AzureBaseConfig, self).__init__(thread_config)

    def _is_provider(self, provider_name):
        if provider_name == 'azure':
            return True
        else:
            return False
