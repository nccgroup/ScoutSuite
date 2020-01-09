from ScoutSuite.providers.azure.authentication_strategy import AzureCredentials
from ScoutSuite.providers.azure.facade.aad import AADFacade
from ScoutSuite.providers.azure.facade.arm import ARMFacade
from ScoutSuite.providers.azure.facade.keyvault import KeyVaultFacade
from ScoutSuite.providers.azure.facade.network import NetworkFacade
from ScoutSuite.providers.azure.facade.securitycenter import SecurityCenterFacade
from ScoutSuite.providers.azure.facade.sqldatabase import SQLDatabaseFacade
from ScoutSuite.providers.azure.facade.storageaccounts import StorageAccountsFacade
from ScoutSuite.providers.azure.facade.virtualmachines import VirtualMachineFacade

from azure.mgmt.resource import SubscriptionClient

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

        self.credentials = credentials
        self.subscriptions = None

        self.aad = AADFacade(credentials.graphrbac_credentials, credentials.tenant_id, credentials.subscription_id)
        self.arm = ARMFacade(credentials.credentials, credentials.subscription_id)
        self.keyvault = KeyVaultFacade(credentials.credentials, credentials.subscription_id)
        self.virtualmachines = VirtualMachineFacade(credentials.credentials, credentials.subscription_id)
        self.network = NetworkFacade(credentials.credentials, credentials.subscription_id)
        self.securitycenter = SecurityCenterFacade(credentials.credentials, credentials.subscription_id)
        self.sqldatabase = SQLDatabaseFacade(credentials.credentials, credentials.subscription_id)
        self.storageaccounts = StorageAccountsFacade(credentials.credentials, credentials.subscription_id)

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

    async def get_subscriptions(self):
        # FIXME this is a bogus implementation
        if not self.subscriptions:
            subscription_client = SubscriptionClient(self.credentials.credentials)
            self.subscriptions = list(subscription_client.subscriptions.list())
        return self.subscriptions
