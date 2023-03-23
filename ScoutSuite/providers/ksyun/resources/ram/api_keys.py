
from ScoutSuite.providers.ksyun.resources.base import KsyunResources
from ScoutSuite.providers.ksyun.facade.base import KsyunFacade


class ApiKeys(KsyunResources):
    def __init__(self, facade: KsyunFacade, user):
        super().__init__(facade)
        self.user = user

    async def fetch_all(self):
        for raw_user_api_key in await self.facade.ram.get_user_api_keys(username=self.user['name']):
            id, api_key = await self._parse_api_key(raw_user_api_key)
            self[id] = api_key

    async def _parse_api_key(self, raw_api_key):
        api_key = {}
        api_key['id'] = raw_api_key['AccessKeyId']
        api_key['creation_datetime'] = raw_api_key['CreateDate']
        api_key['status'] = raw_api_key['Status']
        api_key['last_usage_datetime'] = raw_api_key['AkLastUsedTime']
        return api_key['id'], api_key
