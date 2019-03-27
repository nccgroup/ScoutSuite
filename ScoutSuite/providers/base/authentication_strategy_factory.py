from ScoutSuite.providers.aws.authentication_strategy import AWSAuthenticationStrategy
from ScoutSuite.providers.gcp.authentication_strategy import GCPAuthenticationStrategy
from ScoutSuite.providers.azure.authentication_strategy import AzureAuthenticationStrategy

_strategies = {
    'aws': AWSAuthenticationStrategy,
    'gcp': GCPAuthenticationStrategy,
    'azure': AzureAuthenticationStrategy
}


def get_authentication_strategy(provider: str):
    return _strategies[provider]()
