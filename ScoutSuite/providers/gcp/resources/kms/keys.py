from datetime import datetime, timezone

import dateutil

from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.gcp.resources.base import GCPCompositeResources
from ScoutSuite.providers.gcp.resources.kms.kms_policy import KMSPolicy


class Keys(GCPCompositeResources):
    _children = [
        (KMSPolicy, 'kms_iam_policy')
    ]

    def __init__(self, facade: GCPFacade, project_id: str, keyring_name: str, location: str):
        super().__init__(facade)
        self.project_id = project_id
        self.keyring_name = keyring_name
        self.location = location

    async def fetch_all(self):
        raw_keys = await self.facade.kms.list_keys(self.project_id, self.location, self.keyring_name)
        for raw_key in raw_keys:
            key_id, key = self._parse_key(raw_key)
            self[key_id] = key

        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={key_id: {'project_id': self.project_id, 'keyring_name': self.keyring_name,
                             'location': self.location, 'key_name': key['id']}
                    for key_id, key in self.items()})

    def _parse_key(self, raw_key):
        key_dict = {}

        key_dict['id'] = raw_key['name'].split('/')[-1]
        key_dict['state'] = raw_key.get('primary', {}).get('state', None)
        key_dict['creation_datetime'] = raw_key.get('primary', {}).get('createTime', None)
        key_dict['protection_level'] = raw_key.get('primary', {}).get('protectionLevel', None)
        key_dict['algorithm'] = raw_key.get('primary', {}).get('algorithm', None)
        key_dict['next_rotation_datetime'] = raw_key.get('nextRotationTime', None)
        key_dict['purpose'] = raw_key['purpose']

        key_dict['rotation_period'] = raw_key.get('rotationPeriod', None)
        if key_dict['rotation_period']:
            rotation_period = int("".join(filter(str.isdigit, key_dict['rotation_period'])))
            # get values in days instead of seconds
            key_dict['rotation_period'] = rotation_period//(24*3600)

        key_dict['next_rotation_time_days'] = None
        if key_dict['next_rotation_datetime']:
            next_rotation_time = dateutil.parser.parse(key_dict['next_rotation_datetime']) - datetime.now(timezone.utc)
            key_dict['next_rotation_time_days'] = next_rotation_time.days
        return key_dict['id'], key_dict
