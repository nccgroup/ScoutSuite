
from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class KsyunCredentials:
    def __init__(self, credentials):
        self.credentials = credentials


class KsyunAuthenticationStrategy(AuthenticationStrategy):
    def authenticate(self, access_key_id=None, access_key_secret=None, **kwargs):
        try:

            access_key_id = access_key_id if access_key_id else input('Access Key ID:')
            access_key_secret = access_key_secret if access_key_secret else input('Secret Access Key:')

            credentials = 'credentials'

            return KsyunCredentials(credentials)

        except Exception as e:
            raise AuthenticationException(e)