from ScoutSuite.providers.oci.facade.base import OracleFacade
from ScoutSuite.providers.oci.resources.base import OracleCompositeResources
from ScoutSuite.providers.oci.resources.kms.keys import Keys
from ScoutSuite.providers.utils import get_non_provider_id


class KeyVaults(OracleCompositeResources):

    _children = [
        (Keys, 'keys')
    ]

    def __init__(self, facade: OracleFacade):
        super().__init__(facade)

    async def fetch_all(self):
        raw_keyvaults = await self.facade.kms.get_vaults()
        for raw_keyvault in raw_keyvaults:
            id, keyvault = self._parse_keyvault(raw_keyvault)
            self[id] = keyvault

        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={keyvault_id: {'keyvault': keyvault}
                    for keyvault_id, keyvault in self.items()}
        )


    def _parse_keyvault(self, raw_keyvault):
        keyvault_dict = {}
        keyvault_dict['id'] = get_non_provider_id(raw_keyvault.id)
        keyvault_dict['identifier'] = raw_keyvault.id
        keyvault_dict['name'] = raw_keyvault.display_name
        keyvault_dict['compartment_id'] = raw_keyvault.compartment_id
        keyvault_dict['lifecycle_state'] = raw_keyvault.lifecycle_state
        keyvault_dict['crypto_endpoint'] = raw_keyvault.crypto_endpoint
        keyvault_dict['time_created'] = raw_keyvault.time_created
        keyvault_dict['vault_type'] = raw_keyvault.vault_type
        keyvault_dict['management_endpoint'] = raw_keyvault.management_endpoint
        keyvault_dict['defined_tags'] = list(raw_keyvault.defined_tags)
        keyvault_dict['freeform_tags'] = list(raw_keyvault.freeform_tags)
        return keyvault_dict['id'], keyvault_dict
