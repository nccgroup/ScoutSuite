from aliyunsdkcore.auth.credentials import AccessKeyCredential
from getpass import getpass

from aliyunsdkcore.client import AcsClient
from ScoutSuite.core.console import print_error
from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy


class AliyunCredentials:

    def __init__(self, credentials, client):
        self.credentials = credentials
        self.client = client

class AliyunAuthenticationStrategy(AuthenticationStrategy):
    """
    Implements authentication for the AWS provider
    """

    def authenticate(self, access_key_id, access_key_secret, **kwargs):

        access_key_id = access_key_id if access_key_id else input('Access Key ID:')
        access_key_secret = access_key_secret if access_key_secret else getpass('Secret Access Key:')

        credentials = AccessKeyCredential(access_key_id=access_key_id, access_key_secret=access_key_secret)

        # apiClient = AcsClient(ak='TODO', secret='TODO', region_id='cn-hangzhou')
        # client = AcsClient(credential=credentials)

        # if credentials.get('access_key') is None:
        #     print_error('Failed to authenticate to AWS')
        #     return False

        return credentials

