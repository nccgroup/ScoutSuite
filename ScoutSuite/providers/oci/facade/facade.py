from ScoutSuite.providers.oci.facade.identity import IdentityFacade
from ScoutSuite.providers.oci.authentication_strategy import OracleCredentials


class OracleFacade:
    def __init__(self, credentials: OracleCredentials):
        self.identity = IdentityFacade(credentials)
