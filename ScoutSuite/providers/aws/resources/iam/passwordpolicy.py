from ScoutSuite.providers.aws.resources.base import AWSResources
from botocore.exceptions import ClientError


class PasswordPolicy(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_password_policy = await self.facade.iam.get_password_policy()
        password_policy = self._parse_password_policy(raw_password_policy)
        self.update(password_policy)

    def _parse_password_policy(self, raw_password_policy):
        if 'PasswordReusePrevention' not in raw_password_policy:
            raw_password_policy['PasswordReusePrevention'] = False
        else:
            raw_password_policy['PreviousPasswordPrevented'] = raw_password_policy['PasswordReusePrevention']
            raw_password_policy['PasswordReusePrevention'] = True
        # There is a bug in the API: ExpirePasswords always returns false
        if 'MaxPasswordAge' in raw_password_policy:
            raw_password_policy['ExpirePasswords'] = True

        return raw_password_policy
