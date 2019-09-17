from ScoutSuite.providers.os.facade.base import OpenstackFacade
from ScoutSuite.providers.os.resources.keystone.base import Keystone
from ScoutSuite.providers.base.services import BaseServicesConfig


class OpenstackServicesConfig(BaseServicesConfig):

    def __init__(self, credentials=None, **kwargs):

        super(OpenstackServicesConfig, self).__init__(credentials)

        facade = OpenstackFacade(credentials)

        self.keystone = Keystone(facade)

    def _is_provider(self, provider_name):
        return provider_name == 'os'
