from ScoutSuite.providers.aliyun.resources.base import AliyunResources
from ScoutSuite.providers.aliyun.facade.facade import AliyunFacade


class ApiKeys(AliyunResources):
    def __init__(self, facade: AliyunFacade, user):
        super(ApiKeys, self).__init__(facade)
        self.user = user

    async def fetch_all(self):
        for raw_user_api_key in await self.facade.iam.get_user_api_keys(username=self.user['name']):
            id, api_key = self._parse_api_key(raw_user_api_key)
            self[id] = api_key

    def _parse_api_key(self, raw_api_key):
        api_key = {}
        api_key['id'] = raw_api_key['AccessKeyId']
        api_key['creation_datetime'] = raw_api_key['CreateDate']
        api_key['status'] = raw_api_key['Status']

        return api_key['id'], api_key
