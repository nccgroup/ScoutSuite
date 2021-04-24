from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.utils import get_partition_name, format_arn
from ScoutSuite.providers.utils import get_non_provider_id


class Policies(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region
        self.partition = get_partition_name(facade.session)
        self.service = 'elb'
        self.resource_type = 'policy'

    async def fetch_all(self):
        raw_policies = await self.facade.elb.get_policies(self.region)
        for raw_policy in raw_policies:
            id, policy = self._parse_policy(raw_policy)
            self[id] = policy

    def _parse_policy(self, raw_policy):
        raw_policy['name'] = raw_policy.pop('PolicyName')
        raw_policy['arn'] = format_arn(self.partition, self.service, self.region, '', raw_policy['name'], self.resource_type)
        raw_policy['id'] = get_non_provider_id(raw_policy['name'])

        return raw_policy['id'], raw_policy

