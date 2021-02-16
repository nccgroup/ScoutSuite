from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class SecurityGroups(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_security_groups = await self.facade.elasticache.get_security_groups(self.region)
        parsing_error_counter = 0

        for raw_security_group in raw_security_groups:
            try:
                name, resource = self._parse_security_group(raw_security_group)
                self[name] = resource
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_security_group(self, raw_security_group):
        raw_security_group['name'] = raw_security_group.pop('CacheSecurityGroupName')
        return raw_security_group['name'], raw_security_group
