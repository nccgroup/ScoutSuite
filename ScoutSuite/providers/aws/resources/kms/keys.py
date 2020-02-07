from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class Keys(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(Keys, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_keys = await self.facade.kms.get_keys(self.region)
        for raw_key in raw_keys:
            id, key = self._parse_key(raw_key)
            self[id] = key

    def _parse_key(self, raw_key):
        key_dict = {
            'key_id': raw_key.get('KeyId'),
            'arn': raw_key.get('KeyArn')
        }
        return key_dict['key_id'], key_dict
