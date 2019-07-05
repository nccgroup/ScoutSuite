from ScoutSuite.providers.oci.resources.base import OracleResources
from ScoutSuite.providers.oci.facade.base import OracleFacade


class Keys(OracleResources):
    def __init__(self, facade: OracleFacade):
        super(Keys, self).__init__(facade)

    async def fetch_all(self):

        namespace = await self.facade.objectstorage.get_namespace()

        for raw_key in await self.facade.kms.get_keys():
            id, key = await self._parse_key(raw_key)
            self[id] = key

    async def _parse_key(self, raw_key):
        pass
