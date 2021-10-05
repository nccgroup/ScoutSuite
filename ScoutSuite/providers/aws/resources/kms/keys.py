from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from ScoutSuite.providers.utils import get_non_provider_id
from .grants import Grants


class Keys(AWSCompositeResources):
    _children = [
        (Grants, 'grants'),
    ]

    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_keys = await self.facade.kms.get_keys(self.region)
        for raw_key in raw_keys:
            key_id, key = await self._parse_key(raw_key)
            self[key_id] = key

        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={key_id: {'region': self.region, 'key_id': key['id']}
                    for (key_id, key) in self.items()}
        )

    async def _parse_key(self, raw_key):
        key_dict = {}
        key_dict['id'] = key_dict['name'] = raw_key.get('KeyId')
        key_dict['arn'] = raw_key.get('KeyArn')
        key_dict['policy'] = raw_key.get('policy')

        if 'metadata' in raw_key:
            key_dict['creation_date'] = raw_key['metadata']['KeyMetadata']['CreationDate'] if \
                raw_key['metadata']['KeyMetadata']['CreationDate'] else None
            key_dict['key_enabled'] = False if raw_key['metadata']['KeyMetadata']['KeyState'] in \
                ['Disabled', 'PendingDeletion'] else True
            key_dict['description'] = raw_key['metadata']['KeyMetadata']['Description'] if len(
                raw_key['metadata']['KeyMetadata']['Description'].strip()) > 0 else None
            key_dict['origin'] = raw_key['metadata']['KeyMetadata']['Origin'] if len(
                raw_key['metadata']['KeyMetadata']['Origin'].strip()) > 0 else None
            key_dict['key_manager'] = raw_key['metadata']['KeyMetadata']['KeyManager'] if len(
                raw_key['metadata']['KeyMetadata']['KeyManager'].strip()) > 0 else None

        # Handle keys who don't have these keys - seen in the wild, unsure why
        if 'origin' not in key_dict.keys() or 'key_manager' not in key_dict.keys():
            key_dict['rotation_enabled'] = None
        # Only call this on customer managed CMKs, otherwise the AWS set policies might disallow access and it's always
        # enabled anyway
        elif key_dict['origin'] == 'AWS_KMS' and key_dict['key_manager'] == 'CUSTOMER':
            rotation_status = await self.facade.kms.get_key_rotation_status(self.region, key_dict['id'])
            if rotation_status:
                key_dict['rotation_enabled'] = rotation_status.get('KeyRotationEnabled', None)
            else:
                key_dict['rotation_enabled'] = None
        else:
            key_dict['rotation_enabled'] = True

        key_dict['aliases'] = []
        for raw_alias in raw_key.get('aliases', []):
            key_dict['aliases'].append(self._parse_alias(raw_alias))

        return key_dict['id'], key_dict

    def _parse_alias(self, raw_alias):
        alias_dict = {
            # all KMS Aliases are prefixed with alias/, so we'll strip that off
            'id': get_non_provider_id(raw_alias.get('AliasArn')),
            'name': raw_alias.get('AliasName').split('alias/', 1)[-1],
            'arn': raw_alias.get('AliasArn'),
            'key_id': raw_alias.get('TargetKeyId')}
        return alias_dict
