from ScoutSuite.providers.aws.resources.base import AWSResources


class SecurityGroups(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_security_groups = await self.facade.elasticache.get_security_groups(self.scope['region'])

        for raw_security_group in raw_security_groups:
            name, resource = self._parse_security_group(raw_security_group)
            self[name] = resource

    def _parse_security_group(self, raw_security_group):
        raw_security_group['name'] = raw_security_group.pop('CacheSecurityGroupName')
        return raw_security_group['name'], raw_security_group
