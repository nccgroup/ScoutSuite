from ScoutSuite.providers.aliyun.resources.base import AliyunResources
from ScoutSuite.providers.aliyun.facade.base import AliyunFacade


class PasswordPolicy(AliyunResources):
    def __init__(self, facade: AliyunFacade):
        super(PasswordPolicy, self).__init__(facade)

    async def fetch_all(self):
        raw_password_policy = await self.facade.ram.get_password_policy()
        password_policy = self._parse_password_policy(raw_password_policy)
        self.update(password_policy)

    def _parse_password_policy(self, raw_password_policy):
        password_policy_dict = {
            'minimum_password_length': raw_password_policy.get('MinimumPasswordLength'),
            'hard_expiry': raw_password_policy.get('HardExpiry'),
            'max_login_attempts': raw_password_policy.get('MaxLoginAttemps'),
            'max_password_age': raw_password_policy.get('MaxPasswordAge'),
            'password_reuse_prevention': raw_password_policy.get('PasswordReusePrevention'),
            'require_uppercase_characters': raw_password_policy.get('RequireUppercaseCharacters'),
            'require_lowercase_characters': raw_password_policy.get('RequireLowercaseCharacters'),
            'require_numbers': raw_password_policy.get('RequireNumbers'),
            'require_symbols': raw_password_policy.get('RequireSymbols'),
        }

        if password_policy_dict['password_reuse_prevention'] == 0:
            password_policy_dict['password_reuse_prevention'] = False
        else:
            password_policy_dict['password_reuse_prevention'] = True
            password_policy_dict['password_reuse_count'] = raw_password_policy.get('PasswordReusePrevention')

        return password_policy_dict
