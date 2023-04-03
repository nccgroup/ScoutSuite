import json

import requests

from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class KsyunCredentials:

    def __init__(self, credentials_id, credentials_secret, credentials_cookie, account_id):
        self.credentials_id = credentials_id
        self.credentials_secret = credentials_secret
        self.credentials_cookie = credentials_cookie
        self.account_id = account_id


class KsyunAuthenticationStrategy(AuthenticationStrategy):
    """
    Implements authentication for the Kingsoft Cloud provider
    """

    def authenticate(self, access_key_id=None, access_key_secret=None, access_key_cookie=None, **kwargs):

        try:
            access_key_id = access_key_id if access_key_id else input('Access Key ID:')
            access_key_secret = access_key_secret if access_key_secret else input('Secret Access Key:')
            access_key_cookie = access_key_cookie if access_key_cookie else input('Cookie Key Value:')
            account_id = self.get_user(access_key_cookie)
            return KsyunCredentials(access_key_id, access_key_secret, access_key_cookie, account_id)

        except Exception as e:
            raise AuthenticationException(e)

    def get_user(self, access_key_cookie):
        url = "https://account.console.ksyun.com/i/console/user/get_user"
        headers = {
            "Accept": "application/json",
            "Cookie": access_key_cookie
        }
        r = requests.get(url, headers=headers)
        account_id = json.loads(r.text).get("data").get("user").get("id")
        if account_id:
            return account_id
        else:
            return None