from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.core.console import print_exception


class Users(Resources):
    def __init__(self, facade: GCPFacade, project_id: str, instance_name: str):
        super().__init__(facade)
        self.project_id = project_id
        self.instance_name = instance_name

    async def fetch_all(self):
        raw_users = await self.facade.cloudsql.get_users(self.project_id, self.instance_name)
        parsing_error_counter = 0
        for raw_user in raw_users:
            try:
                user_name, user = self._parse_user(raw_user)
                self[user_name] = user
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_user(self, raw_user):
        user_dict = {}
        user_dict['name'] = raw_user['name']
        user_dict['host'] = raw_user.get('host')
        return user_dict['name'], user_dict
