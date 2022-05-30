from ScoutSuite.providers.openstack.authentication_strategy import OpenstackCredentials
from munch import Munch

# TODO: These methods contain blocking/non-awaitable calls
class KeystoneFacade:
    def __init__(self, credentials: OpenstackCredentials):
        self._credentials = credentials

    async def get_domains(self):
        raw_domains = self._credentials.session.identity.domains()
        return raw_domains

    async def get_groups(self):
        raw_groups = self._credentials.session.identity.groups()
        return  raw_groups

    async def get_policies(self):
        raw_policies = self._credentials.session.identity.policies()
        return raw_policies

    async def get_projects(self):
        raw_projects = self._credentials.session.identity.projects()
        return raw_projects

    async def get_regions(self):
        raw_regions = self._credentials.session.identity.regions()
        return raw_regions

    async def get_users(self):
        raw_users_with_options = []
        raw_users = self._credentials.session.identity.users()
        for raw_user in raw_users:
            raw_user = Munch(raw_user)
            options = await self.get_user_options(raw_user.id)
            raw_user.update({'options': options})
            raw_users_with_options.append(raw_user)
        return raw_users_with_options

    async def get_user_options(self, user_id):
        user = self._credentials.session.get_user_by_id(user_id, normalize=False)
        return user.options

    async def is_fernet(self):
        token = self._credentials.session.auth_token
        return token[:6] == 'gAAAAA'
