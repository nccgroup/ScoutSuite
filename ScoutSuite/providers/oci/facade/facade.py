from ScoutSuite.providers.azure.facade.keyvault import KeyVaultFacade
from ScoutSuite.providers.azure.facade.network import NetworkFacade
from ScoutSuite.providers.azure.facade.securitycenter import SecurityCenterFacade
from ScoutSuite.providers.azure.facade.sqldatabase import SQLDatabaseFacade
from ScoutSuite.providers.azure.facade.storageaccounts import StorageAccountsFacade
from ScoutSuite.providers.azure.authentication_strategy import AzureCredentials

try:
    from ScoutSuite.providers.azure.facade.appgateway_private import AppGatewayFacade
    from ScoutSuite.providers.azure.facade.appservice_private import AppServiceFacade
    from ScoutSuite.providers.azure.facade.loadbalancer_private import LoadBalancerFacade
    from ScoutSuite.providers.azure.facade.rediscache_private import RedisCacheFacade
except ImportError:
    pass


class AzureFacade():
    def __init__(self, credentials: AzureCredentials):
        self.keyvault = KeyVaultFacade(credentials.credentials, credentials.subscription_id)
        self.network = NetworkFacade(credentials.credentials, credentials.subscription_id)
        self.securitycenter = SecurityCenterFacade(credentials.credentials, credentials.subscription_id)
        self.sqldatabase = SQLDatabaseFacade(credentials.credentials, credentials.subscription_id)
        self.storageaccounts = StorageAccountsFacade(credentials.credentials, credentials.subscription_id)

        try:
            self.appgateway = AppGatewayFacade(credentials.credentials, credentials.subscription_id)
            self.appservice = AppServiceFacade(credentials.credentials, credentials.subscription_id)
            self.loadbalancer = LoadBalancerFacade(credentials.credentials, credentials.subscription_id)
            self.rediscache = RedisCacheFacade(credentials.credentials, credentials.subscription_id)
        except NameError:
            pass
