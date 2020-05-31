from ScoutSuite.providers.aliyun.resources.base import AliyunResources
from ScoutSuite.providers.aliyun.facade.base import AliyunFacade


class Keys(AliyunResources):
    def __init__(self, facade: AliyunFacade, region: str):
        super(Keys, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        for raw_key in await self.facade.kms.get_keys(region=self.region):
            id, key = await self._parse_key(raw_key)
            self[id] = key

    async def _parse_key(self, raw_key):
        key_dict = {}
        key_dict['id'] = raw_key.get('KeyId')
        key_dict['name'] = raw_key.get('KeyId')
        key_dict['arn'] = raw_key.get('KeyArn')

        # get additional details for the key
        raw_key_details = await self.facade.kms.get_key_details(key_dict['id'], region=self.region)

        key_dict['creation_date'] = raw_key_details.get('CreationDate')
        key_dict['delete_date'] = raw_key_details.get('DeleteDate')
        key_dict['origin'] = raw_key_details.get('Origin')
        key_dict['description'] = raw_key_details.get('Description')
        key_dict['creator'] = raw_key_details.get('Creator')
        key_dict['usage'] = raw_key_details.get('KeyUsage')
        key_dict['material_expire_time'] = raw_key_details.get('MaterialExpireTime')
        key_dict['state'] = raw_key_details.get('KeyState')

        if key_dict['delete_date'] == '':
            key_dict['delete_date'] = None
        if key_dict['material_expire_time'] == '':
            key_dict['material_expire_time'] = None

        return key_dict['id'], key_dict

