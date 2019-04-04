import json

from ScoutSuite.providers.aws.resources.base import AWSResources


class IdentityPolicies(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_policies = await self.facade.ses.get_identity_policies(self.scope['region'], self.scope['identity_name'])
        for policy_name, raw_policy in raw_policies.items():
            self[policy_name] = json.loads(raw_policy)
