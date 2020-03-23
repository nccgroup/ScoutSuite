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
        group_dict = {}
        group_dict['id'] = group_dict['name'] = raw_group.get('GroupName')
        group_dict['comments'] = raw_group.get('Comments')
        group_dict['create_date'] = raw_group.get('CreateDate')
        group_dict['update_date'] = raw_group.get('UpdateDate')

        group_dict['users'] = []
        for raw_user in await self.facade.ram.get_group_users(group_dict['name']):
            group_dict['users'].append({
                'name': raw_user.get('UserName'),
                'display_name': raw_user.get('DisplayName'),
                'join_date': raw_user.get('JoinDate')
            })

        return group_dict['id'], group_dict

