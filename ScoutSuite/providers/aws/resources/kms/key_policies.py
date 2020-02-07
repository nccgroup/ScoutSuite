from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class KeyPolicies(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(KeyPolicies, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_key_policies = await self.facade.kms.get_key_policies(self.region)
        for raw_key_policy in raw_key_policies:
            key_id, policy = self._parse_key_policy(raw_key_policy)
            self[key_id] = policy

    def _parse_key_policy(self, raw_key_policy):
        key_policy_dict = {
            'id': get_non_provider_id(raw_key_policy.get('PolicyNames')),
            'policy_names': raw_key_policy.get('PolicyNames')

        }
        return key_policy_dict['id'], key_policy_dict
