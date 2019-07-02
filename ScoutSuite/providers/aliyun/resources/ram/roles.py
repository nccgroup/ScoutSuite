from ScoutSuite.providers.aliyun.resources.base import AliyunResources
from ScoutSuite.providers.aliyun.facade.base import AliyunFacade


class Roles(AliyunResources):
    def __init__(self, facade: AliyunFacade):
        super(Roles, self).__init__(facade)

    async def fetch_all(self):
        for raw_role in await self.facade.ram.get_roles():
            id, role = await self._parse_role(raw_role)
            self[id] = role

    async def _parse_role(self, raw_role):
        role_dict = {}
        role_dict['identifier'] = raw_role.get('RoleId')  # required as groups use the name as an ID
        role_dict['id'] = role_dict['name'] = raw_role.get('RoleName')
        role_dict['create_date'] = raw_role.get('CreateDate')
        role_dict['description'] = raw_role.get('Description')
        role_dict['arn'] = raw_role.get('Arn')
        return role_dict['id'], role_dict


