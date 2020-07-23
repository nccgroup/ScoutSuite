import os
from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy

class BambooHRAuthenticationStrategy(AuthenticationStrategy):
    """
    Implements authentication for the AWS provider
    """

    def authenticate(self, **kwargs):
        return os.environ.get("BAMBOOHR_TOKEN")
