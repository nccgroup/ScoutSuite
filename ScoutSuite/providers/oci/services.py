from ScoutSuite.providers.oci.authentication_strategy import OracleCredentials
from ScoutSuite.providers.oci.facade.base import OracleFacade
from ScoutSuite.providers.oci.resources.identity.base import Identity
from ScoutSuite.providers.base.services import BaseServicesConfig


class OracleServicesConfig(BaseServicesConfig):
    def __init__(self, credentials: OracleCredentials = None, **kwargs):
        super(OracleServicesConfig, self).__init__(credentials)

        facade = OracleFacade(credentials)

        self.identity = Identity(facade)

    def _is_provider(self, provider_name):
        return provider_name == 'oci'
