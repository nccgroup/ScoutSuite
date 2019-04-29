import boto3

from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class AWSAuthenticationStrategy(AuthenticationStrategy):
    """
    Implements authentication for the AWS provider
    """

    def authenticate(self, profile=None, **kwargs):

        try:

            session = boto3.Session(profile_name=profile)
            credentials = session.get_credentials().__dict__

            # Test querying for current user
            sts_client = session.client('sts')
            sts_client.get_caller_identity()

            return credentials

        except Exception as e:
            raise AuthenticationException(e)
