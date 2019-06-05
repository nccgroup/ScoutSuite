from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.gcp import GCPFacade


class KeyRings(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super(KeyRings, self).__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_key_rings = await self.facade.kms.list_key_rings(self.project_id)
        for raw_key_ring in raw_key_rings:
            key_ring_id, key_ring = self._parse_key_ring(raw_key_ring)
            self[key_ring_id] = key_ring

    def _parse_key_ring(self, raw_key_ring):
        key_ring_dict = {}
        key_ring_dict['id'] = raw_key_ring.name
        key_ring_dict['name'] = raw_key_ring.name.split('/')[-1]
        # key_ring_dict[''] = raw_key_ring.
        # key_ring_dict[''] = raw_key_ring.
        # key_ring_dict[''] = raw_key_ring.
        # key_ring_dict[''] = raw_key_ring.
        return key_ring_dict['id'], key_ring_dict
