# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.providers.azure.services.storageaccounts import StorageAccountsConfig
from ScoutSuite.providers.azure.services.monitor import MonitorConfig


class AzureServicesConfig(BaseServicesConfig):

    def __init__(self, metadata=None, thread_config=4, **kwargs):

        self.storageaccounts = StorageAccountsConfig(thread_config=thread_config)
        self.monitor = MonitorConfig(thread_config=thread_config)

    def _is_provider(self, provider_name):
        return provider_name == 'azure'
