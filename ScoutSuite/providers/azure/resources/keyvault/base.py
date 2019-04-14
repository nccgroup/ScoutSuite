from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class KeyVaults(AzureResources):
    async def fetch_all(self):
        self['vaults'] = {}
        for raw_vault in await self.facade.keyvault.get_key_vaults():
            id, vault = self._parse_key_vault(raw_vault)
            self['vaults'][id] = vault

        self['vaults_count'] = len(self['vaults'])

    def _parse_key_vault(self, raw_vault):
        vault = {}
        vault['id'] = get_non_provider_id(raw_vault.id)
        vault['name'] = raw_vault.name
        vault['public_access_allowed'] = self._is_public_access_allowed(raw_vault)

        return vault['id'], vault

    def _is_public_access_allowed(self, raw_vault):
        return raw_vault.properties.network_acls is None
