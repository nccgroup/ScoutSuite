from ScoutSuite.providers.oci.resources.base import OracleResources
from ScoutSuite.providers.oci.facade.base import OracleFacade


class PasswordPolicy(OracleResources):
    def __init__(self, facade: OracleFacade):
        super().__init__(facade)

    async def fetch_all(self):
        raw_authentication_policy = await self.facade.identity.get_authentication_policy()
        if raw_authentication_policy:
            password_policy = self._parse_authentication_policy(raw_authentication_policy)
        else:
            password_policy = {}
        self.update(password_policy)

    def _parse_authentication_policy(self, raw_authentication_policy):
        password_policy_dict = {}
        password_policy_dict['is_username_containment_allowed'] = \
            raw_authentication_policy.password_policy.is_username_containment_allowed
        password_policy_dict['is_uppercase_characters_required'] = \
            raw_authentication_policy.password_policy.is_uppercase_characters_required
        password_policy_dict['is_lowercase_characters_required'] = \
            raw_authentication_policy.password_policy.is_lowercase_characters_required
        password_policy_dict['is_special_characters_required'] = \
            raw_authentication_policy.password_policy.is_special_characters_required
        password_policy_dict['minimum_password_length'] = \
            raw_authentication_policy.password_policy.minimum_password_length
        password_policy_dict['is_numeric_characters_required'] = \
            raw_authentication_policy.password_policy.is_numeric_characters_required
        return password_policy_dict


