from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.azure.facade.keyvault import KeyVaultFacade
from ScoutSuite.providers.utils import get_non_provider_id


class KeyVaults(Resources):

    async def fetch_all(self, credentials, **kwargs):
        # TODO: build that facade somewhere else:
        facade = KeyVaultFacade(credentials.credentials, credentials.subscription_id)

        self['vaults'] = {}
        for raw_vault in await facade.get_key_vaults():
            id, vault = self._parse(raw_vault)
            self['vaults'][id] = vault

        self['vaults_count'] = len(self['vaults'])

    def _parse(self, raw_vault):
        vault = {}
        vault['id'] = get_non_provider_id(raw_vault.id)
        vault['name'] = raw_vault.name
        vault['public_access_allowed'] = self._is_public_access_allowed(raw_vault)

        return vault['id'], vault

    def _is_public_access_allowed(self, raw_vault):
        return raw_vault.properties.network_acls is None
