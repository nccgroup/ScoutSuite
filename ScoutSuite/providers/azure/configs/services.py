# -*- coding: utf-8 -*-

from ScoutSuite.providers.azure.authentication_strategy import AzureCredentials
from ScoutSuite.providers.azure.facade.facade import AzureFacade
from ScoutSuite.providers.azure.resources.keyvault.key_vaults import KeyVaults
from ScoutSuite.providers.azure.resources.network.networks import Networks
from ScoutSuite.providers.azure.resources.securitycenter.security_center import SecurityCenter
from ScoutSuite.providers.azure.resources.sqldatabase.servers import Servers
from ScoutSuite.providers.azure.resources.storageaccounts.storageaccounts import StorageAccounts
from ScoutSuite.providers.base.configs.services import BaseServicesConfig

try:
    from ScoutSuite.providers.azure.resources.appgateway_private.application_gateways_private import ApplicationGateways
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.resources.rediscache_private.redis_caches_private import RedisCaches
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.resources.appservice_private.web_applications_private import WebApplications
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.resources.loadbalancer_private.load_balancers_private import LoadBalancers
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
        except NameError:
            pass
        try:
            self.rediscache = RedisCaches(facade)
        except NameError:
            pass
        try:
            self.appservice = WebApplications(facade)
        except NameError:
            pass
        try:
            self.loadbalancer = LoadBalancers(facade)
        except NameError:
            pass

    def _is_provider(self, provider_name):
        return provider_name == 'azure'
