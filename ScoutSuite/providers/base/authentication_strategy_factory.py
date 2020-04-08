_strategies = {
    'aws': 'AWSAuthenticationStrategy',
    'gcp': 'GCPAuthenticationStrategy',
    'azure': 'AzureAuthenticationStrategy',
    'aliyun': 'AliyunAuthenticationStrategy',
    'oci': 'OracleAuthenticationStrategy'
}


def import_authentication_strategy(provider):
    strategy_class = _strategies[provider]
    module = __import__('ScoutSuite.providers.{}.authentication_strategy'.format(provider), fromlist=[strategy_class])
    authentication_strategy = getattr(module, strategy_class)
    return authentication_strategy


def get_authentication_strategy(provider: str):
    """
        Returns an authentication strategy implementation for a provider.
        :param provider: The authentication strategy 
    """
    authentication_strategy = import_authentication_strategy(provider)
    return authentication_strategy()
