import boto3

from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException
from ScoutSuite.providers.aws.utils import get_caller_identity


class AWSCredentials:

    def __init__(self, session):
        self.session = session


class AWSAuthenticationStrategy(AuthenticationStrategy):
    """
    Implements authentication for the AWS provider
    """

    def authenticate(self, profile=None, **kwargs):

        try:

            session = boto3.Session(profile_name=profile)

            # # Test querying for current user
            identity = get_caller_identity(session)

            return AWSCredentials(session=session)

        except Exception as e:
            raise AuthenticationException(e)
