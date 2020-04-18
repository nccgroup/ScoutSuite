from ScoutSuite.providers.oci.resources.base import OracleResources
from ScoutSuite.providers.oci.facade.base import OracleFacade
from ScoutSuite.providers.utils import get_non_provider_id


class Keys(OracleResources):
    def __init__(self, facade: OracleFacade, keyvault):
        super(Keys, self).__init__(facade)
        self.key_vault = keyvault

    async def fetch_all(self):

        for raw_key in await self.facade.kms.get_keys(self.key_vault):
            id, key = await self._parse_key(raw_key)
            self[id] = key

    async def _parse_key(self, raw_key):
        key_dict = {}
        key_dict['id'] = get_non_provider_id(raw_key.id)
        key_dict['identifier'] = raw_key.id
        key_dict['name'] = raw_key.display_name
        key_dict['vault_id'] = raw_key.vault_id
        key_dict['lifecycle_state'] = raw_key.lifecycle_state
        key_dict['compartment_id'] = raw_key.compartment_id
        key_dict['time_created'] = raw_key.time_created
        key_dict['defined_tags'] = list(raw_key.defined_tags)
        key_dict['freeform_tags'] = list(raw_key.freeform_tags)
        return key_dict['id'], key_dict
