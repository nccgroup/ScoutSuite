from ScoutSuite.providers.azure.authentication_strategy import AzureCredentials
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.keyvault.base import KeyVaults
from ScoutSuite.providers.azure.resources.network.base import Networks
from ScoutSuite.providers.azure.resources.securitycenter.base import SecurityCenter
from ScoutSuite.providers.azure.resources.sqldatabase.base import Servers
from ScoutSuite.providers.azure.resources.storageaccounts.base import StorageAccounts
from ScoutSuite.providers.base.configs.services import BaseServicesConfig

# Try to import proprietary services
try:
    from ScoutSuite.providers.azure.resources.private_appgateway.base import ApplicationGateways
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.resources.private_rediscache.base import RedisCaches
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.resources.appservice_private.base import WebApplications
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.resources.private_loadbalancer.base import LoadBalancers
except ImportError:
    pass


class AzureServicesConfig(BaseServicesConfig):

    def __init__(self, credentials: AzureCredentials = None, **kwargs):
        super(AzureServicesConfig, self).__init__(credentials)
        facade = AzureFacade(credentials)

        self.storageaccounts = StorageAccounts(facade)
        self.securitycenter = SecurityCenter(facade)
        self.sqldatabase = Servers(facade)
        self.network = Networks(facade)
        self.keyvault = KeyVaults(facade)

        try:
            self.appgateway = ApplicationGateways(facade)
        except NameError as _:
            pass
        try:
            self.rediscache = RedisCaches(facade)
        except NameError as _:
            pass
        try:
            self.appservice = WebApplications(facade)
        except NameError as _:
            pass
        try:
            self.loadbalancer = LoadBalancers(facade)
        except NameError as _:
            pass

    def _is_provider(self, provider_name):
        return provider_name == 'azure'
