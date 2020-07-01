from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.utils import get_non_provider_id


class Users(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_bindings = await self.facade.cloudresourcemanager.get_member_bindings(self.project_id)
        parsed_users = self._parse_binding(raw_bindings)
        for user_id in parsed_users.keys():
            self[parsed_users[user_id]['id']] = parsed_users[user_id]

    def _parse_binding(self, raw_bindings):

        parsed_users = {}
        for binding in raw_bindings:
            role = binding['role'].split('/')[-1]
            if 'members' in binding:
                for member in binding['members']:
                    member_type, entity = member.split(':')[:2]
                    if member_type == 'user':
                        if entity not in parsed_users.keys():
                            parsed_users[entity] = {'id': get_non_provider_id(entity),
                                                    'name': entity,
                                                    'roles': [role]}
                        else:
                            parsed_users[entity]['roles'].append(role)
        return parsed_users
