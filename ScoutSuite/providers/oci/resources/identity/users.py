from ScoutSuite.providers.oci.resources.base import OracleCompositeResources
from ScoutSuite.providers.oci.facade.facade import OracleFacade
from ScoutSuite.providers.oci.resources.utils import get_non_provider_id

from .api_keys import ApiKeys


class Users(OracleCompositeResources):
    _children = [
        (ApiKeys, 'api_keys')
    ]

    def __init__(self, facade: OracleFacade):
        self.facade = facade

    async def fetch_all(self):
        for raw_user in await self.facade.identity.get_users():
            id, user = self._parse_user(raw_user)
            self[id] = user

        await self._fetch_children_of_all_resources(
            resources=self,
            kwargs={user_id: {'user': user,
                              'facade': self.facade}
                    for user_id, user in self.items()}
        )

    def _parse_user(self, raw_user):
        user = {}
        user['id'] = get_non_provider_id(raw_user.id)
        user['identifier'] = raw_user.id
        user['name'] = raw_user.name
        user['mfa_activated'] = raw_user.is_mfa_activated

        return user['id'], user
