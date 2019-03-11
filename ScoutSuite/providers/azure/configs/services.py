# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.providers.azure.services.storageaccounts import StorageAccountsConfig
from ScoutSuite.providers.azure.services.monitor import MonitorConfig
from ScoutSuite.providers.azure.resources.sqldatabase.servers import Servers as SQLDatabaseConfig
from ScoutSuite.providers.azure.services.securitycenter import SecurityCenterConfig
from ScoutSuite.providers.azure.services.network import NetworkConfig
from ScoutSuite.providers.azure.services.keyvault import KeyVaultConfig
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

    def __init__(self, metadata=None, thread_config=4, **kwargs):

        self.storageaccounts = StorageAccountsConfig(thread_config=thread_config)
        self.monitor = MonitorConfig(thread_config=thread_config)
        self.sqldatabase = SQLDatabaseConfig()
        self.securitycenter = SecurityCenterConfig(thread_config=thread_config)
        self.network = NetworkConfig(thread_config=thread_config)
        self.keyvault = KeyVaultConfig(thread_config=thread_config)

        try:
            self.appgateway = ApplicationGateways()
        except NameError:
            pass
        try:
            self.rediscache = RedisCaches()
        except NameError:
            pass
        try:
            self.appservice = WebApplications()
        except NameError:
            pass
        try:
            self.loadbalancer = LoadBalancers()
        except NameError:
            pass

    def _is_provider(self, provider_name):
        return provider_name == 'azure'
