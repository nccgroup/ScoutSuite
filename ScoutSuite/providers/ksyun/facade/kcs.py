import json

from ksyun.common.common_client import CommonClient
from ksyun.common import credential
from ksyun.common.exception.ksyun_sdk_exception import KsyunSDKException
from ksyun.common.profile.client_profile import ClientProfile
from ksyun.common.profile.http_profile import HttpProfile

from ScoutSuite.providers.ksyun.authentication_strategy import KsyunCredentials


class KCSFacade:
    def __init__(self, credentials: KsyunCredentials):
        self._credentials = credentials

    async def get_clusters(self, region):

        try:
            cred = credential.Credential(self._credentials.credentials_id, self._credentials.credentials_secret)

            httpProfile = HttpProfile()
            httpProfile.endpoint = "kcs.api.ksyun.com"
            httpProfile.reqMethod = "GET"
            httpProfile.reqTimeout = 60
            httpProfile.scheme = "http"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile

            common_client = CommonClient("kcs", '2016-07-01', cred, region, profile=clientProfile)
            r = common_client.call("DescribeCacheClusters", {})
            response = json.loads(r).get('Data')
            if response:
                return response
            else:
                return []
        except KsyunSDKException as err:
            return []
