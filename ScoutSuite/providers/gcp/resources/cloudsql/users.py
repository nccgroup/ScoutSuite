from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade


class Users(Resources):
    def __init__(self, facade: GCPFacade, project_id: str, instance_name: str):
        super(Users, self).__init__(facade)
        self.project_id = project_id
        self.instance_name = instance_name

    async def fetch_all(self):
        raw_users = await self.facade.cloudsql.get_users(self.project_id, self.instance_name)
        for raw_user in raw_users:
            user_name, user = self._parse_user(raw_user)
            self[user_name] = user

    def _parse_user(self, raw_user):
        user_dict = {}
        user_dict['name'] = raw_user['name']
        user_dict['host'] = raw_user.get('host')
        return user_dict['name'], user_dict
