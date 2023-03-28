import json

from ksyun.common.common_client import CommonClient
from ksyun.common import credential
from ksyun.common.exception.ksyun_sdk_exception import KsyunSDKException
from ksyun.common.profile.client_profile import ClientProfile
from ksyun.common.profile.http_profile import HttpProfile

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.ksyun.authentication_strategy import KsyunCredentials


class KKMSFacade:
    def __init__(self, credentials: KsyunCredentials):
        self._credentials = credentials

    async def get_keys(self, region):
        """
        Get all keys

        :return: a list of all keys
        """
        try:
            cred = credential.Credential(self._credentials.credentials_id, self._credentials.credentials_secret)

            httpProfile = HttpProfile()
            httpProfile.endpoint = "kkms.api.ksyun.com"
            httpProfile.reqMethod = "POST"
            httpProfile.reqTimeout = 60
            httpProfile.scheme = "http"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile

            common_client = CommonClient("kkms", '2016-03-04', cred, region, profile=clientProfile)
            r = common_client.call("DescribeKeys", {})
            response = json.loads(r).get('KeySet')
            if response:
                return response
            else:
                return []
        except KsyunSDKException as err:
            print(err)
            return []

    async def get_key_details(self, key_id, region):
        """
        Gets details for a key

        :return: a dictionary of details
        """
        try:
            response = ''
            if response:
                return response['KeyMetadata']
            else:
                return []
        except Exception as e:
            print_exception(f'Failed to get KMS key details: {e}')
            return []
