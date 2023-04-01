from ScoutSuite.providers.ksyun.facade.base import KsyunFacade
from ScoutSuite.providers.ksyun.resources.actiontrail.base import ActionTrail
from ScoutSuite.providers.ksyun.resources.ram.base import RAM
from ScoutSuite.providers.ksyun.resources.kec.base import KEC
from ScoutSuite.providers.ksyun.resources.rds.base import RDS
from ScoutSuite.providers.ksyun.resources.vpc.base import VPC
from ScoutSuite.providers.ksyun.resources.kkms.base import KKMS
from ScoutSuite.providers.ksyun.resources.ks3.base import KS3
from ScoutSuite.providers.ksyun.resources.slb.base import SLB
from ScoutSuite.providers.base.services import BaseServicesConfig


class KsyunServicesConfig(BaseServicesConfig):
    def __init__(self, credentials, **kwargs):
        super().__init__(credentials)

        facade = KsyunFacade(credentials)
        # self.actiontrail = ActionTrail(facade)
        # self.kec = KEC(facade)
        # self.kkms = KKMS(facade)
        # self.rds = RDS(facade)
        # self.ram = RAM(facade)
        # self.vpc = VPC(facade)
        # self.ks3 = KS3(facade)
        self.slb = SLB(facade)

    def _is_provider(self, provider_name):
        return provider_name == 'ksyun'
