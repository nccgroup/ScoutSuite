from ScoutSuite.providers.aliyun.resources.base import AliyunCompositeResources
from ScoutSuite.providers.aliyun.resources.ram.users import Users
from ScoutSuite.providers.aliyun.resources.ram.password_policy import PasswordPolicy
from ScoutSuite.providers.aliyun.resources.ram.security_policy import SecurityPolicy


class RAM(AliyunCompositeResources):
    _children = [
        (Users, 'users'),
        (PasswordPolicy, 'password_policy'),
        (SecurityPolicy, 'security_policy')
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)

        # We do not want the report to count the password policies as resources,
        # they aren't really resources.
        self['password_policy_count'] = 0
        self['security_policy_count'] = 0

        # TODO for each user check last login & API key usage for "last activity"
