import json
from getpass import getpass

from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.client import AcsClient
from aliyunsdksts.request.v20150401 import GetCallerIdentityRequest

from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class AliyunCredentials:

    def __init__(self, credentials, caller_details):
        self.credentials = credentials
        self.caller_details = caller_details


class AliyunAuthenticationStrategy(AuthenticationStrategy):
    """
    Implements authentication for the AWS provider
    """

    def authenticate(self, access_key_id=None, access_key_secret=None, **kwargs):

        try:

            access_key_id = access_key_id if access_key_id else input('Access Key ID:')
            access_key_secret = access_key_secret if access_key_secret else getpass('Secret Access Key:')

            credentials = AccessKeyCredential(access_key_id=access_key_id, access_key_secret=access_key_secret)

            # get caller details
            client = AcsClient(credential=credentials)
            response = client.do_action_with_exception(
                GetCallerIdentityRequest.GetCallerIdentityRequest())
            response_decoded = json.loads(response)

            return AliyunCredentials(credentials, response_decoded)

        except Exception as e:
            raise AuthenticationException(e)
