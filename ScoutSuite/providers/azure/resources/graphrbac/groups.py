from ScoutSuite.providers.azure.resources.base import AzureResources


class Groups(AzureResources):
    async def fetch_all(self):
        for raw_group in await self.facade.graphrbac.get_groups():
            id, group = self._parse_group(raw_group)
            self[id] = group

    def _parse_group(self, raw_group):
        group_dict = {}
        return group_dict['id'], group_dict
