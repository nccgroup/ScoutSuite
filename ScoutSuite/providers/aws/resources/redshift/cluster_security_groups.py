from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class ClusterSecurityGroups(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(ClusterSecurityGroups, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_security_groups = await self.facade.redshift.get_cluster_security_groups(self.region)
        for raw_security_group in raw_security_groups:
            id, security_group = self._parse_security_group(raw_security_group)
            self[id] = security_group

    def _parse_security_group(self, raw_security_group):
        name = raw_security_group.pop('ClusterSecurityGroupName')
        raw_security_group['name'] = name
        return name, raw_security_group
