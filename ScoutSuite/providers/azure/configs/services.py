# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.providers.azure.services.storageaccounts import StorageAccountsConfig
try:
    from ScoutSuite.providers.azure.services.monitor_private import MonitorConfig
except ImportError:
    pass


class AzureServicesConfig(BaseServicesConfig):

    def __init__(self, metadata=None, thread_config=4, **kwargs):

        self.storageaccounts = StorageAccountsConfig(thread_config=thread_config)
        try:
            self.monitor = MonitorConfig(thread_config=thread_config)
        except NameError:
            pass

    def _is_provider(self, provider_name):
        return provider_name == 'azure'
