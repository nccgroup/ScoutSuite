from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.oci.facade.facade import OracleFacade


class Users(Resources):

    def __init__(self, facade: OracleFacade):
        self.facade = facade

    async def fetch_all(self, **kwargs):
        self['users'] = {}
        for raw_user in await self.facade.identity.get_users():
            id, user = self._parse_user(raw_user)
            self['users'][id] = user

        self['users_count'] = len(self['users'])

    def _parse_user(self, raw_user):
        user = {}
        user['id'] = raw_user.id
        user['name'] = raw_user.name
        user['mfa_activated'] = raw_user.is_mfa_activated

        return user['id'], user

