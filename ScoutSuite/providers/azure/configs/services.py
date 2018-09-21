# -*- coding: utf-8 -*-

from opinel.utils.console import printError, printException, printDebug

from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.providers.azure.services.storageaccounts import StorageAccountsConfig

class AzureServicesConfig(BaseServicesConfig):

    def __init__(self, metadata=None, thread_config=4, **kwargs):

        self.storageaccounts = StorageAccountsConfig(thread_config=thread_config)

    def _is_provider(self, provider_name):
        if provider_name == 'azure':
            return True
        else:
            return False
