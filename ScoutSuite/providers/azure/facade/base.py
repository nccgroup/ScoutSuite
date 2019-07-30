from ScoutSuite.providers.azure.authentication_strategy import AzureCredentials
from ScoutSuite.providers.azure.facade.graphrbac import GraphRBACFacade
from ScoutSuite.providers.azure.facade.keyvault import KeyVaultFacade
from ScoutSuite.providers.azure.facade.network import NetworkFacade
from ScoutSuite.providers.azure.facade.securitycenter import SecurityCenterFacade
from ScoutSuite.providers.azure.facade.sqldatabase import SQLDatabaseFacade
from ScoutSuite.providers.azure.facade.storageaccounts import StorageAccountsFacade
from ScoutSuite.providers.azure.facade.virtualmachines import VirtualMachineFacade

# Try to import proprietary services
try:
    from ScoutSuite.providers.azure.facade.appgateway_private import AppGatewayFacade
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.facade.appservice_private import AppServiceFacade
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.facade.loadbalancer_private import LoadBalancerFacade
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.facade.rediscache_private import RedisCacheFacade
except ImportError:
    pass


class AzureFacade():
    def __init__(self, credentials: AzureCredentials):
        self.keyvault = KeyVaultFacade(credentials.credentials, credentials.subscription_id)
        self.virtualmachines = VirtualMachineFacade(credentials.credentials, credentials.subscription_id)
        self.network = NetworkFacade(credentials.credentials, credentials.subscription_id)
        self.securitycenter = SecurityCenterFacade(credentials.credentials, credentials.subscription_id)
        self.sqldatabase = SQLDatabaseFacade(credentials.credentials, credentials.subscription_id)
        self.storageaccounts = StorageAccountsFacade(credentials.credentials, credentials.subscription_id)
        self.graphrbac = GraphRBACFacade(credentials.graphrbac_credentials, credentials.tenant_id)

        # Instantiate facades for proprietary services
        try:
            self.appgateway = AppGatewayFacade(credentials.credentials, credentials.subscription_id)
        except NameError:
            pass
        try:
            self.appservice = AppServiceFacade(credentials.credentials, credentials.subscription_id)
        except NameError:
            pass
        try:
            self.loadbalancer = LoadBalancerFacade(credentials.credentials, credentials.subscription_id)
        except NameError:
            pass
        try:
            self.rediscache = RedisCacheFacade(credentials.credentials, credentials.subscription_id)
        except NameError:
            pass
