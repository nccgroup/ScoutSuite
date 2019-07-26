from ScoutSuite.providers.oci.resources.base import OracleCompositeResources
from ScoutSuite.providers.oci.resources.identity.users import Users
from ScoutSuite.providers.oci.resources.identity.groups import Groups
from ScoutSuite.providers.oci.resources.identity.policies import Policies
from ScoutSuite.providers.oci.resources.identity.authentication_policy import PasswordPolicy
from ScoutSuite.providers.oci.facade.base import OracleFacade


class Identity(OracleCompositeResources):
    _children = [
        (Users, 'users'),
        (Groups, 'groups'),
        (Policies, 'policies'),
        (PasswordPolicy, 'password_policy')
    ]

    def __init__(self, facade: OracleFacade):
        super(Identity, self).__init__(facade)
        self.service = 'identity'

    async def fetch_all(self, **kwargs):
        await self._fetch_children(resource_parent=self)

        # We do not want the report to count the password policies as resources,
        # they aren't really resources.
        self['password_policy_count'] = 0

    async def finalize(self):
        self._match_users_and_groups()
        self._set_user_names_to_group_members()
        return

    def _match_users_and_groups(self):
        """
        Parses the users and groups to match
        :return: None
        """
        for user in self['users']:
            self['users'][user]['groups'] = []
            for group in self['groups']:
                if any(u['user_identifier'] == self['users'][user]['identifier'] for u in self['groups'][group]['users']):
                    self['users'][user]['groups'].append(self['groups'][group])

    def _set_user_names_to_group_members(self):
        """
        Parses the users and groups to match user names
        :return: None
        """
        for group in self['groups']:
            for user in self['groups'][group]['users']:
                user['user_name'] = self['users'][user['user_id']]['name']




