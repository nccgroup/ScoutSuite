from ScoutSuite.providers.openstack.authentication_strategy import OpenstackCredentials


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
        raw_users = self._credentials.session.identity.users()
        return raw_users

    async def is_fernet(self):
        token = self._credentials.session.auth_token
        return token[:6] == 'gAAAAA'
