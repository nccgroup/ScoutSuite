from aliyunsdkcore.auth.credentials import AccessKeyCredential
from getpass import getpass
import json

from aliyunsdkcore.client import AcsClient
from ScoutSuite.core.console import print_error
from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException

from aliyunsdksts.request.v20150401 import GetCallerIdentityRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException


class AliyunCredentials:

    def __init__(self, credentials, client, caller_details):
        self.credentials = credentials
        self.client = client
        self.caller_details = caller_details

class AliyunAuthenticationStrategy(AuthenticationStrategy):
    """
    Implements authentication for the AWS provider
    """

    def authenticate(self, access_key_id, access_key_secret, **kwargs):

        try:

            access_key_id = access_key_id if access_key_id else input('Access Key ID:')
            access_key_secret = access_key_secret if access_key_secret else getpass('Secret Access Key:')

            credentials = AccessKeyCredential(access_key_id=access_key_id, access_key_secret=access_key_secret)

            client = AcsClient(credential=credentials)

            response = client.do_action_with_exception(GetCallerIdentityRequest.GetCallerIdentityRequest())
            response_decoded = json.loads(response)

            return AliyunCredentials(credentials, client, response_decoded)

        except Exception as e:
            raise AuthenticationException(e)

