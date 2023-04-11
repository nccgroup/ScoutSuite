from ScoutSuite.providers.ksyun.resources.base import KsyunResources
from ScoutSuite.providers.ksyun.facade.base import KsyunFacade


class Keys(KsyunResources):
    def __init__(self, facade: KsyunFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        for raw_key in await self.facade.kkms.get_keys(region=self.region):
            id, key = await self._parse_key(raw_key)
            self[id] = key

    async def _parse_key(self, raw_key):
        key_dict = {}
        key_dict['id'] = raw_key.get('KeyId')
        key_dict['name'] = raw_key.get('KeyName')
        key_dict['creation_date'] = raw_key.get('CreateTime')
        key_dict['description'] = raw_key.get('Description')
        key_dict['state'] = raw_key.get('KeyState')
        key_dict['usage'] = raw_key.get('KeyUsage')
        key_dict['origin'] = raw_key.get('Origin')
        key_dict['delete_date'] = None
        key_dict['material_expire_time'] = None
        return key_dict['id'], key_dict
