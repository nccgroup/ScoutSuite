from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.ram import RAMFacade
from ScoutSuite.providers.aliyun.facade.ecs import ECSFacade
from ScoutSuite.providers.aliyun.facade.rds import RDSFacade
from ScoutSuite.providers.aliyun.facade.vpc import VPCFacade
from ScoutSuite.providers.aliyun.facade.actiontrail import ActiontrailFacade
from ScoutSuite.providers.aliyun.facade.kms import KMSFacade
from ScoutSuite.providers.utils import run_concurrently

from collections import Counter
from aliyunsdkcore.endpoint import EndpointResolver

class AliyunFacade:
    def __init__(self, credentials: AliyunCredentials):
        self._credentials = credentials
        self._instantiate_facades()

    def _instantiate_facades(self):
        self.actiontrail = ActiontrailFacade(self._credentials)
        self.ram = RAMFacade(self._credentials)
        self.ecs = ECSFacade(self._credentials)
        self.rds = RDSFacade(self._credentials)
        self.vpc = VPCFacade(self._credentials)
        self.kms = KMSFacade(self._credentials)

    async def build_region_list(self, service: str, chosen_regions=None):

        # TODO could need this for service ids
        # service = 'ec2containerservice' if service == 'ecs' else service

        # TODO does a similar endpoint exist?
        # available_services = await run_concurrently(lambda: Session().get_available_services())
        # if service not in available_services:
        #     raise Exception('Service ' + service + ' is not available.')

        regions = \
            await run_concurrently(lambda: Session().get_available_regions(service, partition_name))

        if chosen_regions:
            return list((Counter(regions) & Counter(chosen_regions)).elements())
        else:
            return regions
