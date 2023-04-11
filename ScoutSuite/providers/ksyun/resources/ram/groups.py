from ScoutSuite.providers.ksyun.resources.base import KsyunResources
from ScoutSuite.providers.ksyun.facade.base import KsyunFacade


class Groups(KsyunResources):
    def __init__(self, facade: KsyunFacade):
        super().__init__(facade)

    async def fetch_all(self):
        for raw_group in await self.facade.ram.get_groups():
            id, group = await self._parse_group(raw_group)
            self[id] = group

    async def _parse_group(self, raw_group):
        group_dict = {}
        group_dict['krn'] = raw_group.get('Krn')
        group_dict['id'] = raw_group.get('GroupId')
        group_dict['name'] = raw_group.get('GroupName')
        group_dict['user_count'] = raw_group.get('UserCount')
        group_dict['policy_count'] = raw_group.get('PolicyCount')
        group_dict['description'] = raw_group.get('Description')
        group_dict['create_date'] = raw_group.get('CreateDate')

        group_dict['users'] = []
        # for raw_user in await self.facade.ram.get_group_users(group_dict['name']):
        #     group_dict['users'].append({
        #         'name': raw_user.get('UserName'),
        #         'display_name': raw_user.get('DisplayName'),
        #         'join_date': raw_user.get('JoinDate')
        #     })

        return group_dict['id'], group_dict
