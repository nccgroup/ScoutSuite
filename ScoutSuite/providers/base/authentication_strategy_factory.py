from ScoutSuite.providers.aws.authentication_strategy import AWSAuthenticationStrategy
from ScoutSuite.providers.gcp.authentication_strategy import GCPAuthenticationStrategy
from ScoutSuite.providers.azure.authentication_strategy import AzureAuthenticationStrategy
from ScoutSuite.providers.aliyun.authentication_strategy import AliyunAuthenticationStrategy
from ScoutSuite.providers.oci.authentication_strategy import OracleAuthenticationStrategy
from ScoutSuite.providers.openstack.authentication_strategy import OpenstackAuthenticationStrategy


_strategies = {
    'aws': AWSAuthenticationStrategy,
    'gcp': GCPAuthenticationStrategy,
    'azure': AzureAuthenticationStrategy,
    'aliyun': AliyunAuthenticationStrategy,
    'oci': OracleAuthenticationStrategy,
    'openstack': OpenstackAuthenticationStrategy
}


def get_authentication_strategy(provider: str):
    """
        Returns an authentication strategy implementation for a provider.
        :param provider: The authentication strategy 
    """
    return _strategies[provider]()
