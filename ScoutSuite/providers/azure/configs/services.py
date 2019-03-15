# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.providers.azure.resources.monitor.activity_logs import ActivityLogs
from ScoutSuite.providers.azure.resources.securitycenter.security_center import SecurityCenter
from ScoutSuite.providers.azure.resources.sqldatabase.servers import Servers
from ScoutSuite.providers.azure.resources.storageaccounts.storageaccounts import StorageAccounts
from ScoutSuite.providers.azure.resources.network.networks import Networks
from ScoutSuite.providers.azure.resources.keyvault.key_vaults import KeyVaults
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

        self.monitor = ActivityLogs()
        self.storageaccounts = StorageAccounts()
        self.securitycenter = SecurityCenter()
        self.sqldatabase = Servers()
        self.network = Networks()
        self.keyvault = KeyVaults()

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
