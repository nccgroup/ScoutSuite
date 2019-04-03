# -*- coding: utf-8 -*-

from ScoutSuite.providers.azure.authentication_strategy import AzureCredentials
from ScoutSuite.providers.azure.facade import AzureFacade
from ScoutSuite.providers.azure.resources.keyvault import KeyVaults
from ScoutSuite.providers.azure.resources.network import Networks
from ScoutSuite.providers.azure.resources.securitycenter import SecurityCenter
from ScoutSuite.providers.azure.resources.sqldatabase import Servers
from ScoutSuite.providers.azure.resources.storageaccounts import StorageAccounts
from ScoutSuite.providers.base.configs.services import BaseServicesConfig

try:
    from ScoutSuite.providers.azure.resources.private_appgateway import ApplicationGateways
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.resources.private_rediscache import RedisCaches
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.resources.appservice_private import WebApplications
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.resources.private_loadbalancer import LoadBalancers
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
