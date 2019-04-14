import json

from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class IdentityPolicies(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, identity_name: str):
        super(IdentityPolicies, self).__init__(facade)
        self.region = region
        self.identity_name = identity_name

    async def fetch_all(self):
        raw_policies = await self.facade.ses.get_identity_policies(self.region, self.identity_name)
        for policy_name, raw_policy in raw_policies.items():
            self[policy_name] = json.loads(raw_policy)
