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

    def authenticate(self,
                     profile=None,
                     aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None,
                     **kwargs):

        try:

            if profile:
                session = boto3.Session(profile_name=profile)
            elif aws_access_key_id and aws_secret_access_key:
                if aws_session_token:
                    session = boto3.Session(
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        aws_session_token=aws_session_token,
                    )
                else:
                    session = boto3.Session(
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                    )
            else:
                raise AuthenticationException('Insufficient credentials provided')

            # Test querying for current user
            identity = get_caller_identity(session)

            return AWSCredentials(session=session)

        except Exception as e:
            raise AuthenticationException(e)
