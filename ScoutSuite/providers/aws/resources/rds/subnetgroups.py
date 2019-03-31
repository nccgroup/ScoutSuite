from ScoutSuite.providers.aws.resources.resources import AWSResources


class SubnetGroups(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_subnet_groups = await self.facade.rds.get_subnet_groups(self.scope['region'], self.scope['vpc'])
        for raw_subnet_group in raw_subnet_groups:
            name, resource = self._parse_subnet_group(raw_subnet_group)
            self[name] = resource

    def _parse_subnet_group(self, raw_subnet_group):
        raw_subnet_group['name'] = raw_subnet_group['DBSubnetGroupName']
        return raw_subnet_group['name'], raw_subnet_group
