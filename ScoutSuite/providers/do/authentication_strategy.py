from ScoutSuite.providers.do import utils
from ScoutSuite.providers.base.authentication_strategy import AuthenticationException
from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy
from ScoutSuite.core.console import print_warning
from pydo import Client
import logging
import boto3


class DoCredentials:
    def __init__(self, client, session=None):
        self.client = client
        self.session = session


class DigitalOceanAuthenticationStrategy(AuthenticationStrategy):

    def authenticate(self, token=None, access_key=None, access_secret=None, **kwargs):
        """
        Handles authentication to DigitalOcean.
        """
        try:
            self.client = Client(token)
            # a simple request here to make sure the authentication is successful
            self.client.account.get()

            if not (access_key and access_secret):
                print_warning(
                    f"Missing credentials for spaces: Skipping DO Spaces service"
                )
                return DoCredentials(client=self.client)
            else:
                # Set logging level to error for libraries as otherwise generates a lot of warnings
                logging.getLogger("botocore").setLevel(logging.ERROR)
                logging.getLogger("botocore.auth").setLevel(logging.ERROR)
                logging.getLogger("urllib3").setLevel(logging.ERROR)

                session = boto3.Session(
                    aws_access_key_id=access_key,
                    aws_secret_access_key=access_secret,
                )
                # make sure the DO spaces authentication is successful
                region = "blr1"
                spaces_client = utils.get_client("s3", session, region)
                spaces_client.list_buckets()
                return DoCredentials(client=self.client, session=session)

        except Exception as e:
            raise AuthenticationException(e)
