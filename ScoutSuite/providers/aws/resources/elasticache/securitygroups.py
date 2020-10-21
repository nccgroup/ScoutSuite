from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class SecurityGroups(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_security_groups = await self.facade.elasticache.get_security_groups(self.region)

        for raw_security_group in raw_security_groups:
            try:
                name, resource = self._parse_security_group(raw_security_group)
                self[name] = resource
            except Exception as e:
                print_exception('Failed to parse {} resource: {}'.format(self.__class__.__name__, e))

    def _parse_security_group(self, raw_security_group):
        raw_security_group['name'] = raw_security_group.pop('CacheSecurityGroupName')
        return raw_security_group['name'], raw_security_group
