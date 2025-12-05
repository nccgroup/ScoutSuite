import logging
import json

from oci.config import from_file
from oci.identity import IdentityClient
from oci.auth.signers import InstancePrincipalsSecurityTokenSigner

from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class OracleCredentials:

    def __init__(self, config : dict, signer : InstancePrincipalsSecurityTokenSigner):
        self.config = config
        self.signer = signer

    def get_scope(self):
        
        if self.signer is not None:
            print("get scope called")
            return self.signer.tenancy_id
            print("get scope finished")

        if 'compartment-id' in self.config:
            return self.config['compartment-id']
        else:
            return self.config['tenancy']


class OracleAuthenticationStrategy(AuthenticationStrategy):
    """
    Implements authentication for the AWS provider
    """

    def authenticate(self, profile=None, **kwargs):

        try:

            # Set logging level to error for libraries as otherwise generates a lot of warnings
            logging.getLogger('oci').setLevel(logging.ERROR)
            
            config = {}
            signer = None
            if kwargs["oci_use_inspr"]:
                signer = InstancePrincipalsSecurityTokenSigner()
            else: 
                print(kwargs["oci_use_inspr"])
                config = from_file(profile_name=profile)
            
            # Get the current user
            identity = IdentityClient(config=config, signer=signer)
            print(identity)
            return OracleCredentials(config, signer)

        except Exception as e:
            raise AuthenticationException(e)
