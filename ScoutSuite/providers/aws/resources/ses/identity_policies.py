import json

from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.utils import format_arn


class IdentityPolicies(AWSResources):

    def __init__(self, facade: AWSFacade, region: str, identity_name: str):
        super().__init__(facade)
        self.region = region
        self.identity_name = identity_name
        self.partition = facade.partition
        self.service = 'ses'
        self.resource_type = 'identity-policy'

    async def fetch_all(self):
        raw_policies = await self.facade.ses.get_identity_policies(self.region, self.identity_name)
        for policy_name, raw_policy in raw_policies.items():
            self[policy_name] = json.loads(raw_policy)
            self[policy_name]['arn'] = format_arn(self.partition, self.service, self.region, '', policy_name, self.resource_type)
