from ScoutSuite.providers.aliyun.resources.base import AliyunResources
from ScoutSuite.providers.aliyun.facade.base import AliyunFacade


class Groups(AliyunResources):
    def __init__(self, facade: AliyunFacade):
        super(Groups, self).__init__(facade)

    async def fetch_all(self):
        for raw_group in await self.facade.ram.get_groups():
            id, group = await self._parse_group(raw_group)
            self[id] = group

    async def _parse_group(self, raw_group):
        group = {}
        group['id'] = raw_group['GroupName']
        group['name'] = raw_group['GroupName']
        group['comments'] = raw_group['Comments']
        group['creation_datetime'] = raw_group['CreateDate']
        group['update_datetime'] = raw_group['UpdateDate']
        return group['id'], group
