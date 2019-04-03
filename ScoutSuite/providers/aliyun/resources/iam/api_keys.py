from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.aliyun.facade.facade import AliyunFacade
# from ScoutSuite.providers.aliyun.resources.utils import get_non_provider_id


class ApiKeys(Resources):

    def __init__(self, user, facade: AliyunFacade):
        self.facade = facade
        self.user = user

    async def fetch_all(self, **kwargs):
        for raw_user_api_key in await self.facade.iam.get_user_api_keys(username=self.user['name']):
            id, api_key = self._parse_api_key(raw_user_api_key)
            self[id] = api_key

    def _parse_api_key(self, raw_api_key):
        api_key = {}
        api_key['id'] = raw_api_key['AccessKeyId']
        api_key['creation_datetime'] = raw_api_key['CreateDate']
        api_key['status'] = raw_api_key['Status']

        return api_key['id'], api_key
