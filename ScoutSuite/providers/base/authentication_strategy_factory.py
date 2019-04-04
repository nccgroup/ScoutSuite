from ScoutSuite.providers.aws.authentication_strategy import AWSAuthenticationStrategy
from ScoutSuite.providers.gcp.authentication_strategy import GCPAuthenticationStrategy
from ScoutSuite.providers.azure.authentication_strategy import AzureAuthenticationStrategy

_strategies = {
    'aws': AWSAuthenticationStrategy,
    'gcp': GCPAuthenticationStrategy,
    'azure': AzureAuthenticationStrategy
}


class InvalidAuthenticationStrategyException(Exception): pass


def get_authentication_strategy(provider: str):
    if provider not in _strategies:
        raise InvalidAuthenticationStrategyException()

    return _strategies[provider]()
