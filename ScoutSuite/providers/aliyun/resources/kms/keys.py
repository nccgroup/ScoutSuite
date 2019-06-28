from ScoutSuite.providers.aliyun.resources.base import AliyunResources
from ScoutSuite.providers.aliyun.facade.facade import AliyunFacade


class Keys(AliyunResources):
    def __init__(self, facade: AliyunFacade):
        super(Keys, self).__init__(facade)

    async def fetch_all(self):
        for raw_key in await self.facade.kms.get_keys():
            id, key = await self._parse_key(raw_key)
            self[id] = key

    async def _parse_key(self, raw_key):
        key_dict = {}
        key_dict['id'] = raw_key.get('KeyId')
        key_dict['name'] = raw_key.get('KeyId')
        key_dict['arn'] = raw_key.get('KeyArn')
        return key_dict['id'], key_dict

