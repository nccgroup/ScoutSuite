from ScoutSuite.providers.oci.facade.base import OracleFacade
from ScoutSuite.providers.oci.resources.base import OracleCompositeResources
from ScoutSuite.providers.oci.resources.objectstorage.buckets import Buckets


class ObjectStorage(OracleCompositeResources):
    _children = [
        (Buckets, 'buckets')
    ]

    def __init__(self, facade: OracleFacade):
        super(ObjectStorage, self).__init__(facade)
        self.service = 'objectstorage'

    async def fetch_all(self, **kwargs):
        await self._fetch_children(resource_parent=self)
