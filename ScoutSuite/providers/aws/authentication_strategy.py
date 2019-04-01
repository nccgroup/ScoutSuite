import boto3

from ScoutSuite.core.console import print_error
from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy


class AWSAuthenticationStrategy(AuthenticationStrategy):
    """
    Implements authentication for the AWS provider
    """

    def authenticate(self, profile=None, **kwargs):
        session = boto3.Session(profile_name=profile)
        credentials = session.get_credentials().__dict__

        if credentials.get('access_key') is None:
            print_error('Failed to authenticate to AWS')
            return False

        return credentials
