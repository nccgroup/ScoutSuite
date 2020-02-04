import logging

from oci.config import from_file
from oci.identity import IdentityClient

from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class OracleCredentials:

    def __init__(self, config, compartment_id):
        self.config = config
        self.compartment_id = compartment_id


class OracleAuthenticationStrategy(AuthenticationStrategy):
    """
    Implements authentication for the AWS provider
    """

    def authenticate(self, profile=None, **kwargs):

        try:

            # Set logging level to error for libraries as otherwise generates a lot of warnings
            logging.getLogger('oci').setLevel(logging.ERROR)

            config = from_file(profile_name=profile)
            if 'compartment-id' in config:
                compartment_id = config['compartment-id']
            else:
                compartment_id = config['tenancy']

            # Get the current user
            identity = IdentityClient(config)
            identity.get_user(config["user"]).data

            return OracleCredentials(config, compartment_id)

        except Exception as e:
            raise AuthenticationException(e)
