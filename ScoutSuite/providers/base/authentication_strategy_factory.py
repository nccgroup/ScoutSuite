from ScoutSuite.providers.aws.authentication_strategy import AWSAuthenticationStrategy
from ScoutSuite.providers.gcp.authentication_strategy import GCPAuthenticationStrategy

_strategies = {
    'aws': AWSAuthenticationStrategy,
    'gcp': GCPAuthenticationStrategy
}


def get_authentication_strategy(provider: str):
    return _strategies[provider]()
