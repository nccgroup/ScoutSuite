import json
from ksyun.common.common_client import CommonClient
from ksyun.common import credential
from ksyun.common.exception.ksyun_sdk_exception import KsyunSDKException
from ksyun.common.profile.client_profile import ClientProfile
from ksyun.common.profile.http_profile import HttpProfile

from ScoutSuite.providers.ksyun.authentication_strategy import KsyunCredentials
from ScoutSuite.providers.ksyun.facade.actiontrail import ActiontrailFacade
from ScoutSuite.providers.ksyun.facade.kec import KECFacade
from ScoutSuite.providers.ksyun.facade.ram import RAMFacade
from ScoutSuite.providers.ksyun.facade.rds import RDSFacade
from ScoutSuite.providers.ksyun.facade.vpc import VPCFacade
from ScoutSuite.providers.ksyun.facade.kkms import KKMSFacade


class KsyunFacade:
    def __init__(self, credentials: KsyunCredentials):
        self._credentials = credentials
        self._instantiate_facades()

    def _instantiate_facades(self):
        self.actiontrail = ActiontrailFacade(self._credentials)
        self.kec = KECFacade(self._credentials)
        self.ram = RAMFacade(self._credentials)
        self.rds = RDSFacade(self._credentials)
        self.vpc = VPCFacade(self._credentials)
        self.kkms = KKMSFacade(self._credentials)

    async def build_region_list(self, service: str, chosen_regions=None):

        try:
            regions = []
            cred = credential.Credential(self._credentials.credentials_id, self._credentials.credentials_secret)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "kec.api.ksyun.com"
            httpProfile.reqMethod = "POST"
            httpProfile.reqTimeout = 60
            httpProfile.scheme = "http"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile

            # 用户有权限的机房API
            common_client = CommonClient("kec", '2016-03-04', cred, "cn-beijing-6", profile=clientProfile)
            r = common_client.call("DescribeRegions", {})
            items = json.loads(r).get('RegionSet')
            if items:
                for item in items:
                    regions.append(item['Region'])
                return regions
            else:
                return []
        except KsyunSDKException as err:
            # print(err)
            return []
        
