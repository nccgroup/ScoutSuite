from ScoutSuite.providers.aws.resources.resources import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class SecurityGroups(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_security_groups = await self.facade.rds.get_security_groups(self.scope['region'])
        for raw_security_group in raw_security_groups:
            name, resource = self._parse_security_group(raw_security_group)
            self[name] = resource

    def _parse_security_group(self, raw_security_group):
        raw_security_group['arn'] = raw_security_group.pop('DBSecurityGroupArn')
        raw_security_group['name'] = raw_security_group.pop('DBSecurityGroupName')
        return raw_security_group['name'], raw_security_group
