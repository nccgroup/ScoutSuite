# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.providers.azure.services.storageaccounts import StorageAccountsConfig
from ScoutSuite.providers.azure.services.monitor import MonitorConfig
from ScoutSuite.providers.azure.services.sqldatabase import SQLDatabaseConfig
from ScoutSuite.providers.azure.services.keyvault import KeyVaultConfig
try:
    from ScoutSuite.providers.azure.services.appgateway_private import AppGatewayConfig
except ImportError:
    pass


class AzureServicesConfig(BaseServicesConfig):

    def __init__(self, metadata=None, thread_config=4, **kwargs):

        self.storageaccounts = StorageAccountsConfig(thread_config=thread_config)
        self.monitor = MonitorConfig(thread_config=thread_config)
        self.sqldatabase = SQLDatabaseConfig(thread_config=thread_config)
        self.keyvault = KeyVaultConfig(thread_config=thread_config)

        try:
            self.appgateway = AppGatewayConfig(thread_config=thread_config)
        except NameError:
            pass

    def _is_provider(self, provider_name):
        return provider_name == 'azure'
