from ScoutSuite.providers.openstack.resources.base import OpenstackResources


class Regions(OpenstackResources):
    async def fetch_all(self):
        raw_regions = await self.facade.keystone.get_regions()
        for raw_region in raw_regions:
            id, region = self._parse_region(raw_region)
            if id in self:
                continue

            self[id] = region

    def _parse_region(self, raw_region):
        region_dict = {}
        region_dict['id'] = raw_region.id
        region_dict['description'] = raw_region.description
        region_dict['parent_region'] = raw_region.parent_region_id
        return region_dict['id'], region_dict
