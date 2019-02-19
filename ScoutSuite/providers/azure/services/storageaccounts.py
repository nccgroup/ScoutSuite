# -*- coding: utf-8 -*-

from ScoutSuite.providers.azure.configs.base import AzureBaseConfig
from ScoutSuite.providers.azure.utils import get_resource_group_name

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

        storage_account_dict['id'] = self.get_non_provider_id(storage_account.id.lower())
        storage_account_dict['name'] = storage_account.name
        storage_account_dict['https_traffic_enabled'] = storage_account.enable_https_traffic_only
        storage_account_dict['public_traffic_allowed'] = self._is_public_traffic_allowed(storage_account)
        storage_account_dict['blob_containers'] = self._parse_blob_containers(storage_account)

        self.storage_accounts[storage_account_dict['id']] = storage_account_dict

    def _is_public_traffic_allowed(self, storage_account):
        return storage_account.network_rule_set.default_action == "Allow"

    def _parse_blob_containers(self, storage_account):
        blob_containers = {}
        for container in storage_account.blob_containers:
            container_dict = {}
            container_dict['id'] = container.name
            container_dict['public_access_allowed'] = container.public_access != "None"
            blob_containers[container.name] = container_dict

        return blob_containers

    def _get_targets(self, response_attribute, api_client, method, list_params, ignore_list_error):
        if response_attribute == "Storage Accounts":
            return self._get_storage_accounts(api_client, method, list_params)
        else:
            return super(StorageAccountsConfig, self)._get_targets(response_attribute, api_client, method,
                                                                   list_params, ignore_list_error)

    def _get_storage_accounts(self, api_client, method, list_params):
        storage_accounts = []
        storage_accounts_raw = method(**list_params)
        for storage_account in storage_accounts_raw:
            resource_group_name = get_resource_group_name(storage_account.id)
            setattr(storage_account, "blob_containers", \
                    api_client.blob_containers.list(resource_group_name, storage_account.name).value)
            storage_accounts.append(storage_account)

        return storage_accounts
