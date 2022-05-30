from ScoutSuite.providers.openstack.resources.base import OpenstackResources


class Groups(OpenstackResources):
    async def fetch_all(self):
        raw_groups = await self.facade.keystone.get_groups()
        for raw_groups in raw_groups:
            id, group = self._parse_group(raw_groups)
            if id in self:
                continue

            self[id] = group

    def _parse_group(self, raw_group):
        group_dict = {}
        group_dict['id'] = raw_group.id
        group_dict['name'] = raw_group.name
        group_dict['domain_id'] = raw_group.domain_id
        group_dict['description'] = raw_group.description
        return group_dict['id'], group_dict
