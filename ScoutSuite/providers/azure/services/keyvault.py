# -*- coding: utf-8 -*-

from ScoutSuite.providers.azure.configs.base import AzureBaseConfig


class KeyVaultConfig(AzureBaseConfig):
    targets = (
        ('vaults', 'Key Vaults', 'list_by_subscription', {}, False),
    )

    def __init__(self, thread_config):

        self.vaults = {}
        self.vaults_count = 0

        super(KeyVaultConfig, self).__init__(thread_config)

    def parse_vaults(self, vault, params):
        vault_dict = {}
        vault_dict['id'] = self.get_non_provider_id(vault.id)
        vault_dict['name'] = vault.name
        vault_dict['public_access_allowed'] = self._is_public_access_allowed(vault)

        self.vaults[vault_dict['id']] = vault_dict

    def _is_public_access_allowed(self, vault):
        return vault.properties.network_acls is None
