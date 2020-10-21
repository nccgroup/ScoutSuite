from ScoutSuite.providers.oci.facade.base import OracleFacade
from ScoutSuite.providers.oci.resources.base import OracleResources
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.core.console import print_exception


class ApiKeys(OracleResources):
    def __init__(self, facade: OracleFacade, user):
        super().__init__(facade)
        self.user = user

    async def fetch_all(self):
        for raw_user_api_key in await self.facade.identity.get_user_api_keys(user_id=self.user['identifier']):
            try:
                id, api_key = await self._parse_api_key(raw_user_api_key)
                self[id] = api_key
            except Exception as e:
                print_exception('Failed to parse {} resource: {}'.format(self.__class__.__name__, e))

    async def _parse_api_key(self, raw_api_key):
        api_key = {}
        api_key['id'] = get_non_provider_id(raw_api_key.key_id)
        api_key['identifier'] = raw_api_key.key_id
        api_key['fingerprint'] = raw_api_key.fingerprint
        api_key['state'] = raw_api_key.lifecycle_state
        return api_key['id'], api_key
