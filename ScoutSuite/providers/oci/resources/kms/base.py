from ScoutSuite.providers.oci.facade.base import OracleFacade
from ScoutSuite.providers.oci.resources.base import OracleCompositeResources
from ScoutSuite.providers.oci.resources.kms.keys import Keys


class KMS(OracleCompositeResources):
    _children = [
        (Keys, 'keys')
    ]

    def __init__(self, facade: OracleFacade):
        super(KMS, self).__init__(facade)
        self.service = 'kms'

    async def fetch_all(self, **kwargs):
        await self._fetch_children(resource_parent=self)
