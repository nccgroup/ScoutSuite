from ScoutSuite.providers.salesforce.facade.base import SalesforceFacade
from ScoutSuite.providers.base.services import BaseServicesConfig


class SalesforceServicesConfig(BaseServicesConfig):

    def __init__(self, credentials=None, **kwargs):

        super(SalesforceServicesConfig, self).__init__(credentials)

        facade = SalesforceFacade(credentials)


    def _is_provider(self, provider_name):
        return provider_name == 'salesforce'