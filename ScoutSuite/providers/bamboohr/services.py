from ScoutSuite.providers.bamboohr.facade.base import BambooHRFacade
from ScoutSuite.providers.base.services import BaseServicesConfig
from ScoutSuite.providers.bamboohr.resources.employees import Employees

class BambooHRServicesConfig(BaseServicesConfig):
    """
    Object that holds the necessary BambooHR configuration for all services in scope.
    """

    def __init__(self, credentials=None, **kwargs):
        super(BambooHRServicesConfig, self).__init__(credentials)
        facade = BambooHRFacade(credentials)
        self.employees = Employees(facade)

    def _is_provider(self, provider_name):
        return provider_name == 'bamboohr'
