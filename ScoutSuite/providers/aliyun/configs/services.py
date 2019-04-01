from ScoutSuite.providers.aliyun.facade.facade import AliyunFacade
# from ScoutSuite.providers.azure.resources.keyvault.key_vaults import KeyVaults
# from ScoutSuite.providers.azure.resources.network.networks import Networks
# from ScoutSuite.providers.azure.resources.securitycenter.security_center import SecurityCenter
# from ScoutSuite.providers.azure.resources.sqldatabase.servers import Servers
# from ScoutSuite.providers.azure.resources.storageaccounts.storageaccounts import StorageAccounts
from ScoutSuite.providers.base.configs.services import BaseServicesConfig



class AliyunServicesConfig(BaseServicesConfig):

    def __init__(self, credentials, **kwargs):
        super(AliyunServicesConfig, self).__init__(credentials)
        facade = AliyunFacade(credentials)

        # self.storageaccounts = StorageAccounts(facade)
        # self.securitycenter = SecurityCenter(facade)
        # self.sqldatabase = Servers(facade)
        # self.network = Networks(facade)
        # self.keyvault = KeyVaults(facade)


    def _is_provider(self, provider_name):
        return provider_name == 'aliyun'

