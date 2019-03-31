from ScoutSuite.providers.aws.resources.resources import AWSResources


class ParameterGroups(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_parameter_groups = await self.facade.elasticache.get_parameter_groups(self.scope['region'])
        for raw_parameter_group in raw_parameter_groups:
            name, resource = self._parse_parameter_group(raw_parameter_group)
            self[name] = resource

    def _parse_parameter_group(self, raw_parameter_group):
        raw_parameter_group['name'] = raw_parameter_group.pop('CacheParameterGroupName')
        return raw_parameter_group['name'], raw_parameter_group
