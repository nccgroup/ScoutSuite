from ScoutSuite.providers.base.services import BaseServicesConfig
# from ScoutSuite.providers.osc.resources.api.base import Api
from ScoutSuite.providers.osc.facade.base import OSCFacade
from ScoutSuite.providers.osc.resources.api.base import API

class OSCServicesConfig(BaseServicesConfig):
    """
       Object that holds the necessary OSC configuration for all services in
       scope.

       :ivar api:                          API configuration
       """
    def __init__(self, credentials=None, **kwargs):

        super(OSCServicesConfig, self).__init__(credentials)

        facade = OSCFacade(credentials)

        # self.api = Api(facade)
        self.api = API(facade)

    def _is_provider(self, provider_name):
        return provider_name == 'osc'
