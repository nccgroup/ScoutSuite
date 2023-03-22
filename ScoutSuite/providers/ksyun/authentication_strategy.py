import requests
import datetime

from ScoutSuite.providers.ksyun.utils import sign
from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class KsyunCredentials:

    def __init__(self, credentials_id, credentials_secret):
        self.credentials_id = credentials_id
        self.credentials_secret = credentials_secret


class KsyunAuthenticationStrategy(AuthenticationStrategy):
    """
    Implements authentication for the Kingsoft Cloud provider
    """
    def authenticate(self, access_key_id=None, access_key_secret=None, **kwargs):
        
        try:
            access_key_id = access_key_id if access_key_id else input('Access Key ID:')
            access_key_secret = access_key_secret if access_key_secret else input('Secret Access Key:')
            # params = {
            #     'Accesskey': access_key_id,
            #     'Service': 'iam',
            #     'Action': 'ListUsers',
            #     'Version': '2015-11-01',
            #     'Timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),  # 使用如下的方式产生UTC格式的时间，
            #     'SignatureVersion': '1.0',
            #     'SignatureMethod': 'HMAC-SHA256'
            # }
            # signature = sign(params, access_key_secret)
            # headers = {'Accept': 'application/json'}
            # url = "https://iam.api.ksyun.com/?Signature={}".format(signature)
            # response = requests.get(url, params=params, headers=headers)
            # json_data = response.json()
            return KsyunCredentials(access_key_id, access_key_secret)

        except Exception as e:
            raise AuthenticationException(e)
