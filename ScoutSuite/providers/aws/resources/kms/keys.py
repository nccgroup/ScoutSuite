from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from .grants import Grants
from .key_policies import KeyPolicies


class Keys(AWSCompositeResources):
    _children = [
        (Grants, 'grants'),
        (KeyPolicies, 'key_policies')
    ]

    def __init__(self, facade: AWSFacade, region: str):
        super(Keys, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_keys = await self.facade.kms.get_keys(self.region)
        for raw_key in raw_keys:
            key_id, key = self._parse_key(raw_key)
            self[key_id] = key

        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={key_id: {'region': self.region, 'key_id': key['key_id']}
                    for (key_id, key) in self.items()}
        )

    def _parse_key(self, raw_key):
        key_dict = {
            'key_id': raw_key.get('KeyId'),
            'arn': raw_key.get('KeyArn')
        }
        return key_dict['key_id'], key_dict
