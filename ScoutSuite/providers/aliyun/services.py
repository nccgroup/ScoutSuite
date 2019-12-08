from ScoutSuite.providers.aliyun.facade.base import AliyunFacade
from ScoutSuite.providers.base.services import BaseServicesConfig
from ScoutSuite.providers.aliyun.resources.ram.base import RAM
from ScoutSuite.providers.aliyun.resources.actiontrail.base import ActionTrail
from ScoutSuite.providers.aliyun.resources.vpc.base import VPC
from ScoutSuite.providers.aliyun.resources.ecs.base import ECS
from ScoutSuite.providers.aliyun.resources.rds.base import RDS
from ScoutSuite.providers.aliyun.resources.kms.base import KMS
from ScoutSuite.providers.aliyun.resources.oss.base import OSS



class AliyunServicesConfig(BaseServicesConfig):
    def __init__(self, credentials, **kwargs):
        super(AliyunServicesConfig, self).__init__(credentials)

        facade = AliyunFacade(credentials)

        self.actiontrail = ActionTrail(facade)
        self.ram = RAM(facade)
        self.ecs = ECS(facade)
        self.rds = RDS(facade)
        self.vpc = VPC(facade)
        self.kms = KMS(facade)
        self.oss = OSS(facade)

    def _is_provider(self, provider_name):
        return provider_name == 'aliyun'
