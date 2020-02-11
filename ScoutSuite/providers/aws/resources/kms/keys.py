from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from .grants import Grants


class Keys(AWSCompositeResources):
    _children = [
        (Grants, 'grants'),
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
            scopes={key_id: {'region': self.region, 'key_id': key['id']}
                    for (key_id, key) in self.items()}
        )

    def _parse_key(self, raw_key):
        key_dict = {}
        key_dict['id'] = key_dict['name'] = raw_key.get('KeyId')
        key_dict['arn'] = raw_key.get('KeyArn')
        key_dict['rotation_enabled'] = raw_key['rotation_status']['KeyRotationEnabled'] \
            if 'rotation_status' in raw_key else None

        key_dict['policy'] = raw_key.get('policy')

        if 'metadata' in raw_key:
            key_dict['creation_date'] = raw_key['metadata']['KeyMetadata']['CreationDate'] if \
                raw_key['metadata']['KeyMetadata']['CreationDate'] else None
            key_dict['key_enabled'] = False if raw_key['metadata']['KeyMetadata']['KeyState'] == 'Disabled' else True
            key_dict['description'] = raw_key['metadata']['KeyMetadata']['Description'] if len(
                raw_key['metadata']['KeyMetadata']['Description'].strip()) > 0 else None
            key_dict['origin'] = raw_key['metadata']['KeyMetadata']['Origin'] if len(
                raw_key['metadata']['KeyMetadata']['Origin'].strip()) > 0 else None
            key_dict['key_manager'] = raw_key['metadata']['KeyMetadata']['KeyManager'] if len(
                raw_key['metadata']['KeyMetadata']['KeyManager'].strip()) > 0 else None

        return key_dict['id'], key_dict
