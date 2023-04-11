import json

from ksyun.common.common_client import CommonClient
from ksyun.common import credential
from ksyun.common.exception.ksyun_sdk_exception import KsyunSDKException
from ksyun.common.profile.client_profile import ClientProfile
from ksyun.common.profile.http_profile import HttpProfile

from ScoutSuite.providers.ksyun.authentication_strategy import KsyunCredentials


class VPCFacade:
    def __init__(self, credentials: KsyunCredentials):
        self._credentials = credentials
        self._credentials = credentials
        self.cred = credential.Credential(self._credentials.credentials_id, self._credentials.credentials_secret)

        self.httpProfile = HttpProfile()
        self.httpProfile.endpoint = "vpc.api.ksyun.com"
        self.httpProfile.reqMethod = "POST"
        self.httpProfile.reqTimeout = 60
        self.httpProfile.scheme = "http"

        self.clientProfile = ClientProfile()
        self.clientProfile.httpProfile = self.httpProfile

    async def get_vpcs(self, region):
        """
        Get all VPCs

        :return: a list of all VPCs
        """
        try:
            common_client = CommonClient("vpc", '2016-03-04', self.cred, region, profile=self.clientProfile)
            r = common_client.call("DescribeVpcs", {})
            response = json.loads(r).get('VpcSet')
            if response:
                return response
            else:
                return []
        except KsyunSDKException as err:
            print(err)
            return []

    # async def get_routes(self, vpc_id, region):
    #     try:
    #         cred = credential.Credential(self._credentials.credentials_id, self._credentials.credentials_secret)
    #
    #         httpProfile = HttpProfile()
    #         httpProfile.endpoint = "vpc.api.ksyun.com"
    #         httpProfile.reqMethod = "POST"
    #         httpProfile.reqTimeout = 60
    #         httpProfile.scheme = "http"
    #
    #         clientProfile = ClientProfile()
    #         clientProfile.httpProfile = httpProfile
    #
    #         common_client = CommonClient("vpc", '2016-03-04', cred, region, profile=clientProfile)
    #         r = common_client.call("DescribeRoutes", {"Filter": {"1": {"Name": "vpc-id", "Value": {"1": vpc_id}}}})
    #         response = json.loads(r).get('RouteSet')
    #         if response:
    #             return response
    #         else:
    #             return []
    #     except KsyunSDKException as err:
    #         print(err)
