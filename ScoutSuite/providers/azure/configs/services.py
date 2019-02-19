# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.providers.azure.services.storageaccounts import StorageAccountsConfig
from ScoutSuite.providers.azure.services.monitor import MonitorConfig
from ScoutSuite.providers.azure.services.sqldatabase import SQLDatabaseConfig
from ScoutSuite.providers.azure.services.securitycenter import SecurityCenterConfig
from ScoutSuite.providers.azure.services.network import NetworkConfig
from ScoutSuite.providers.azure.services.keyvault import KeyVaultConfig
try:
    from ScoutSuite.providers.azure.services.appgateway_private import AppGatewayConfig
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.services.rediscache_private import RedisCacheConfig
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.services.appservice_private import AppServiceConfig
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.services.loadbalancer_private import LoadBalancerConfig
except ImportError:
    pass


class AzureServicesConfig(BaseServicesConfig):

    def __init__(self, metadata=None, thread_config=4, **kwargs):

        self.storageaccounts = StorageAccountsConfig(thread_config=thread_config)
        self.monitor = MonitorConfig(thread_config=thread_config)
        self.sqldatabase = SQLDatabaseConfig(thread_config=thread_config)
        self.securitycenter = SecurityCenterConfig(thread_config=thread_config)
        self.network = NetworkConfig(thread_config=thread_config)
        self.keyvault = KeyVaultConfig(thread_config=thread_config)

        try:
            self.appgateway = AppGatewayConfig(thread_config=thread_config)
        except NameError:
            pass
        try:
            self.rediscache = RedisCacheConfig(thread_config=thread_config)
        except NameError:
            pass
        try:
            self.appservice = AppServiceConfig(thread_config=thread_config)
        except NameError:
            pass
        try:
            self.loadbalancer = LoadBalancerConfig(thread_config=thread_config)
        except NameError:
            pass

    def _is_provider(self, provider_name):
        return provider_name == 'azure'
