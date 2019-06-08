from ScoutSuite.providers.aliyun.facade.facade import AliyunFacade
from ScoutSuite.providers.base.services import BaseServicesConfig
from ScoutSuite.providers.aliyun.resources.ram.base import RAM
from ScoutSuite.providers.aliyun.resources.actiontrail.base import ActionTrail
from ScoutSuite.providers.aliyun.resources.vpc.base import VPC


class AliyunServicesConfig(BaseServicesConfig):
    def __init__(self, credentials, **kwargs):
        super(AliyunServicesConfig, self).__init__(credentials)

        facade = AliyunFacade(credentials)

        self.actiontrail = ActionTrail(facade)
        self.ram = RAM(facade)
        self.vpc = VPC(facade)

    def _is_provider(self, provider_name):
        return provider_name == 'aliyun'
