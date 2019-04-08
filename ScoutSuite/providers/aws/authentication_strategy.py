import boto3

from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException

class AWSAuthenticationStrategy(AuthenticationStrategy):
    """
    Implements authentication for the AWS provider
    """
    
    def authenticate(self, profile=None, **kwargs):
        session = boto3.Session(profile_name=profile)
        credentials = session.get_credentials().__dict__

        if credentials.get('access_key') is None:
            raise AuthenticationException()

        return credentials