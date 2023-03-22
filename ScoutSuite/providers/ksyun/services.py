from ScoutSuite.providers.ksyun.facade.base import KsyunFacade
from ScoutSuite.providers.ksyun.resources.kec.base import KEC
from ScoutSuite.providers.ksyun.resources.actiontrail.base import ActionTrail
from ScoutSuite.providers.base.services import BaseServicesConfig


class KsyunServicesConfig(BaseServicesConfig):
    def __init__(self, credentials, **kwargs):
        super().__init__(credentials)

        facade = KsyunFacade(credentials)
        self.actiontrail = ActionTrail(facade)
        self.kec = KEC(facade)

    def _is_provider(self, provider_name):
        return provider_name == 'ksyun'