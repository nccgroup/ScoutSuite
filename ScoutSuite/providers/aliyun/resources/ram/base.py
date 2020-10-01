from ScoutSuite.providers.aliyun.facade.base import AliyunFacade
from ScoutSuite.providers.aliyun.resources.base import AliyunCompositeResources
from ScoutSuite.providers.aliyun.resources.ram.groups import Groups
from ScoutSuite.providers.aliyun.resources.ram.password_policy import PasswordPolicy
from ScoutSuite.providers.aliyun.resources.ram.policies import Policies
from ScoutSuite.providers.aliyun.resources.ram.roles import Roles
from ScoutSuite.providers.aliyun.resources.ram.security_policy import SecurityPolicy
from ScoutSuite.providers.aliyun.resources.ram.users import Users


class RAM(AliyunCompositeResources):
    _children = [
        (Users, 'users'),
        (Groups, 'groups'),
        (Roles, 'roles'),
        (Policies, 'policies'),
        (PasswordPolicy, 'password_policy'),
        (SecurityPolicy, 'security_policy')
    ]

    def __init__(self, facade: AliyunFacade):
        super().__init__(facade)
        self.service = 'ram'

    async def fetch_all(self, **kwargs):
        await self._fetch_children(resource_parent=self)

        # We do not want the report to count the password policies as resources,
        # they aren't really resources.
        self['password_policy_count'] = 0
        self['security_policy_count'] = 0

        # TODO for each user check last login & API key usage for "last activity"

    async def finalize(self):
        self._match_users_and_groups()
        self._match_policies_and_entities()

    def _match_users_and_groups(self):
        """
        Parses the users and groups to match
        :return: None
        """
        for user in self['users']:
            self['users'][user]['groups'] = []
            for group in self['groups']:
                if any(u['name'] == user for u in self['groups'][group]['users']):
                    self['users'][user]['groups'].append(group)

    def _match_policies_and_entities(self):
        for policy in self['policies']:
            for user in self['users']:
                if not self['users'][user].get('policies'):
                    self['users'][user]['policies'] = []
                if self['users'][user]['name'] in self['policies'][policy]['entities'].get('users', []):
                    self['users'][user]['policies'].append(self['policies'][policy]['id'])
        for policy in self['policies']:
            for group in self['groups']:
                if not self['groups'][group].get('policies'):
                    self['groups'][group]['policies'] = []
                if self['groups'][group]['name'] in self['policies'][policy]['entities'].get('groups', []):
                    self['groups'][group]['policies'].append(self['policies'][policy]['id'])
        for policy in self['policies']:
            for role in self['roles']:
                if not self['roles'][role].get('policies'):
                    self['roles'][role]['policies'] = []
                if self['roles'][role]['name'] in self['policies'][policy]['entities'].get('roles', []):
                    self['roles'][role]['policies'].append(self['policies'][policy]['id'])
