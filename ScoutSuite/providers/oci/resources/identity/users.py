from ScoutSuite.providers.oci.resources.base import OracleCompositeResources
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.core.console import print_exception

from .api_keys import ApiKeys


class Users(OracleCompositeResources):
    _children = [
        (ApiKeys, 'api_keys')
    ]

    async def fetch_all(self):
        parsing_error_counter = 0
        for raw_user in await self.facade.identity.get_users():
            try:
                id, user = await self._parse_user(raw_user)
                self[id] = user
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={user_id: {'user': user}
                    for user_id, user in self.items()}
        )

    async def _parse_user(self, raw_user):
        user = {}
        user['identifier'] = raw_user.id
        user['id'] = get_non_provider_id(raw_user.id)
        user['name'] = raw_user.name
        user['identifier'] = raw_user.id
        user['mfa_activated'] = raw_user.is_mfa_activated
        return user['id'], user
