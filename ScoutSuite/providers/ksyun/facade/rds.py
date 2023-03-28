import json

from ksyun.common.common_client import CommonClient
from ksyun.common import credential
from ksyun.common.exception.ksyun_sdk_exception import KsyunSDKException
from ksyun.common.profile.client_profile import ClientProfile
from ksyun.common.profile.http_profile import HttpProfile

from ScoutSuite.providers.ksyun.authentication_strategy import KsyunCredentials


class RDSFacade:
    def __init__(self, credentials: KsyunCredentials):
        self._credentials = credentials
        self.cred = credential.Credential(self._credentials.credentials_id, self._credentials.credentials_secret)

        self.httpProfile = HttpProfile()
        self.httpProfile.endpoint = "krds.api.ksyun.com"
        self.httpProfile.reqMethod = "GET"
        self.httpProfile.reqTimeout = 60
        self.httpProfile.scheme = "http"

        self.clientProfile = ClientProfile()
        self.clientProfile.httpProfile = self.httpProfile

    async def get_instances(self, region):
        """
        Get all instances

        :return: a list of all instances
        """
        try:
            common_client = CommonClient("krds", '2016-07-01', self.cred, region, profile=self.clientProfile)
            r = common_client.call("DescribeDBInstances", {})
            response = json.loads(r).get('Data').get('Instances')
            if response:
                return response
            else:
                return []
        except KsyunSDKException as err:
            print(err)
            return []