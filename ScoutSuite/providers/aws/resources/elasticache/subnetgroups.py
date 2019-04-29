from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class SubnetGroups(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        super(SubnetGroups, self).__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_subnet_groups = await self.facade.elasticache.get_subnet_groups(self.region, self.vpc)
        for raw_subnet_group in raw_subnet_groups:
            name, resource = self._parse_subnet_group(raw_subnet_group)
            self[name] = resource

    def _parse_subnet_group(self, raw_subnet_group):
        raw_subnet_group['name'] = raw_subnet_group.pop('CacheSubnetGroupName')
        return raw_subnet_group['name'], raw_subnet_group
