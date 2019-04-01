from aliyunsdkcore.auth.credentials import AccessKeyCredential

from ScoutSuite.core.console import print_error
from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy


class AliyunAuthenticationStrategy(AuthenticationStrategy):
    """
    Implements authentication for the AWS provider
    """

    def authenticate(self, access_key_id, access_key_secret, **kwargs):

        credentials = AccessKeyCredential(access_key_id=access_key_id, access_key_secret=access_key_secret)

        # if credentials.get('access_key') is None:
        #     print_error('Failed to authenticate to AWS')
        #     return False

        return credentials

