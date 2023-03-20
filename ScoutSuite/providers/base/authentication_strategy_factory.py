_strategies = {
    'aws': 'AWSAuthenticationStrategy',
    'gcp': 'GCPAuthenticationStrategy',
    'azure': 'AzureAuthenticationStrategy',
    'aliyun': 'AliyunAuthenticationStrategy',
    'ksyun': 'KsyunAuthenticationStrategy',
    'oci': 'OracleAuthenticationStrategy'
}


def import_authentication_strategy(provider):
    strategy_class = _strategies[provider]
    module = __import__(f'ScoutSuite.providers.{provider}.authentication_strategy', fromlist=[strategy_class])
    # getattr() 函数用于返回一个对象属性值。 getattr(object, name[, default])
    authentication_strategy = getattr(module, strategy_class)
    return authentication_strategy


# 获取认证策略
def get_authentication_strategy(provider: str):
    """
        Returns an authentication strategy implementation for a provider.
        :param provider: The authentication strategy 
    """
    authentication_strategy = import_authentication_strategy(provider)
    return authentication_strategy()
