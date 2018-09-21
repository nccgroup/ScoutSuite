# -*- coding: utf-8 -*-

from ScoutSuite.providers.azure.configs.base import AzureBaseConfig

from opinel.utils.console import printError, printException, printInfo


class StorageAccountsConfig(AzureBaseConfig):
    targets = (
        ('storage_accounts', 'Storage Accounts', 'list', {}, False),
    )

    def __init__(self, thread_config):

        self.storage_accounts = {}
        self.storage_accounts_count = 0

        super(StorageAccountsConfig, self).__init__(thread_config)

    def parse_storage_accounts(self, storage_account, params):

        storage_account_dict = {}

        storage_account_dict['id'] = self.get_non_provider_id(storage_account.id)
        storage_account_dict['name'] = storage_account.name
        storage_account_dict['https_traffic_enabled'] = 'Enabled' if storage_account.enable_https_traffic_only else 'Disabled'

        self.storage_accounts[storage_account_dict['id']] = storage_account_dict

