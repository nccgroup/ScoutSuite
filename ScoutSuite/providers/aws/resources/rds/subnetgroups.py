from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class SubnetGroups(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        super().__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_subnet_groups = await self.facade.rds.get_subnet_groups(self.region, self.vpc)
        for raw_subnet_group in raw_subnet_groups:
            try:
                name, resource = self._parse_subnet_group(raw_subnet_group)
                self[name] = resource
            except Exception as e:
                print_exception('Failed to parse {} resource: {}'.format(self.__class__.__name__, e))

    def _parse_subnet_group(self, raw_subnet_group):
        raw_subnet_group['name'] = raw_subnet_group['DBSubnetGroupName']
        return raw_subnet_group['name'], raw_subnet_group
