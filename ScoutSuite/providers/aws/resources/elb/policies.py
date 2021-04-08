from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.utils import get_non_provider_id


class Policies(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_policies = await self.facade.elb.get_policies(self.region)
        for raw_policy in raw_policies:
            id, policy = self._parse_policy(raw_policy)
            self[id] = policy

    def _parse_policy(self, raw_policy):
        raw_policy['name'] = raw_policy.pop('PolicyName')
        raw_policy['id'] = get_non_provider_id(raw_policy['name'])
        return raw_policy['id'], raw_policy
