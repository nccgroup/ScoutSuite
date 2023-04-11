from ScoutSuite.providers.ksyun.resources.base import KsyunResources
from ScoutSuite.providers.ksyun.facade.base import KsyunFacade


class PasswordPolicy(KsyunResources):
    def __init__(self, facade: KsyunFacade):
        super().__init__(facade)

    async def fetch_all(self):
        raw_password_policy = await self.facade.ram.get_password_policy()
        password_policy = self._parse_password_policy(raw_password_policy)
        self.update(password_policy)

    def _parse_password_policy(self, raw_password_policy):

        password_policy_dict = {
            'minimum_password_length': raw_password_policy.get('MinLen'),
            'hard_expiry': raw_password_policy.get('SessionExpireTime'),
            'max_login_attempts': raw_password_policy.get('PwdWrongTimes'),
            'max_password_age': raw_password_policy.get('MaxPwdAge'),
            'password_reuse_prevention': raw_password_policy.get('PwdReuse'),
            'require_uppercase_characters': raw_password_policy.get('RequireUpper'),
            'require_lowercase_characters': raw_password_policy.get('RequireLower'),
            'require_numbers': raw_password_policy.get('RequireNum'),
            'require_symbols': raw_password_policy.get('RequireSymbols'),
        }

        if password_policy_dict['password_reuse_prevention'] == 0:
            password_policy_dict['password_reuse_prevention'] = False
        else:
            password_policy_dict['password_reuse_prevention'] = True
            password_policy_dict['password_reuse_count'] = raw_password_policy.get('PwdReuse')

        return password_policy_dict
