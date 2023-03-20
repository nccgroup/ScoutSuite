from ksyun.common.common_client import CommonClient
from ksyun.common import credential
from ksyun.common.exception.ksyun_sdk_exception import KsyunSDKException
from ksyun.common.profile.client_profile import ClientProfile
from ksyun.common.profile.http_profile import HttpProfile

from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class KsyunCredentials:
    def __init__(self, credentials):
        self.credentials = credentials


class KsyunAuthenticationStrategy(AuthenticationStrategy):
    def authenticate(self, access_key_id=None, access_key_secret=None, **kwargs):
        try:
            access_key_id = access_key_id if access_key_id else input('Access Key ID:')
            access_key_secret = access_key_secret if access_key_secret else input('Secret Access Key:')
            cred = credential.Credential(access_key_id, access_key_secret)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "kec.api.ksyun.com"
            httpProfile.reqMethod = "POST"
            httpProfile.reqTimeout = 60
            httpProfile.scheme = "http"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile

            common_client = CommonClient("kec", '2016-03-04', cred, "cn-beijing-6", profile=clientProfile)
            print(common_client.call("DescribeInstances", {"MaxResults": 10}))

            return KsyunCredentials(cred)

        except KsyunSDKException as err:
            raise AuthenticationException(err)