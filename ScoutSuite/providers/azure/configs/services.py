# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.providers.azure.resources.securitycenter.security_center import SecurityCenter
from ScoutSuite.providers.azure.resources.sqldatabase.servers import Servers
from ScoutSuite.providers.azure.resources.storageaccounts.storageaccounts import StorageAccounts
from ScoutSuite.providers.azure.resources.network.networks import Networks
from ScoutSuite.providers.azure.resources.keyvault.key_vaults import KeyVaults
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

    def __init__(self, credentials=None, thread_config=4, **kwargs):

        self.storageaccounts = StorageAccounts()
        self.securitycenter = SecurityCenter()
        self.sqldatabase = Servers()
        self.network = Networks()
        self.keyvault = KeyVaults()

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
