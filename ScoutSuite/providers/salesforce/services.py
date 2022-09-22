from ScoutSuite.providers.salesforce.facade.base import SalesforceFacade
from ScoutSuite.providers.base.services import BaseServicesConfig
from ScoutSuite.providers.salesforce.resources.profiles.base import Profiles


class SalesforceServicesConfig(BaseServicesConfig):

    def __init__(self, credentials=None, **kwargs):

        super(SalesforceServicesConfig, self).__init__(credentials)

        facade = SalesforceFacade(credentials)

        self.profiles = Profiles(facade)


    def _is_provider(self, provider_name):
        return provider_name == 'salesforce'