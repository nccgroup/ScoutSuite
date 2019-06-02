from ScoutSuite.providers.aliyun.facade.facade import AliyunFacade
from ScoutSuite.providers.base.services import BaseServicesConfig
from ScoutSuite.providers.aliyun.resources.iam.base import IAM
from ScoutSuite.providers.aliyun.resources.actiontrail.base import Actiontrail


class AliyunServicesConfig(BaseServicesConfig):
    def __init__(self, credentials, **kwargs):
        super(AliyunServicesConfig, self).__init__(credentials)

        facade = AliyunFacade(credentials)

        self.iam = IAM(facade)
        self.actiontrail = Actiontrail(facade)

    def _is_provider(self, provider_name):
        return provider_name == 'aliyun'
