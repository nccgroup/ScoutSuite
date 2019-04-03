from oci.config import from_file

from ScoutSuite.core.console import print_error
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

            config = from_file(profile_name="test-user")
            compartment_id = config["tenancy"]

            return OracleCredentials(config, compartment_id)

        except Exception as e:
            raise AuthenticationException(e)
