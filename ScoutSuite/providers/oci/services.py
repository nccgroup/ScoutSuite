from ScoutSuite.providers.oci.authentication_strategy import OracleCredentials
from ScoutSuite.providers.oci.facade.base import OracleFacade
from ScoutSuite.providers.oci.resources.identity.base import Identity
from ScoutSuite.providers.oci.resources.kms.base import KMS
from ScoutSuite.providers.oci.resources.objectstorage.base import ObjectStorage
from ScoutSuite.providers.base.services import BaseServicesConfig


class OracleServicesConfig(BaseServicesConfig):
    def __init__(self, credentials: OracleCredentials = None, **kwargs):
        super(OracleServicesConfig, self).__init__(credentials)

        facade = OracleFacade(credentials)

        self.identity = Identity(facade)
        self.objectstorage = ObjectStorage(facade)
        self.kms = KMS(facade)

    def _is_provider(self, provider_name):
        return provider_name == 'oci'
