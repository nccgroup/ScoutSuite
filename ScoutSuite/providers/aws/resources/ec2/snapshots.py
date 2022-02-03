from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.utils import get_name, format_arn


class Snapshots(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region
        self.partition = facade.partition
        self.service = 'ec2'
        self.resource_type = 'snapshot'

    async def fetch_all(self):
        raw_snapshots = await self.facade.ec2.get_snapshots(self.region)
        for raw_snapshot in raw_snapshots:
            name, resource = self._parse_snapshot(raw_snapshot)
            self[name] = resource

    def _parse_snapshot(self, raw_snapshot):
        snapshot_dict = {}
        snapshot_dict['id'] = raw_snapshot.get('SnapshotId')
        snapshot_dict['name'] = get_name(raw_snapshot, raw_snapshot, 'SnapshotId')
        snapshot_dict['description'] = raw_snapshot.get('Description')
        snapshot_dict['public'] = self._is_public(raw_snapshot)
        snapshot_dict['encrypted'] = raw_snapshot.get('Encrypted')
        snapshot_dict['kms_key_id'] = raw_snapshot.get('KmsKeyId')
        snapshot_dict['owner_id'] = raw_snapshot.get('OwnerId')
        snapshot_dict['progress'] = raw_snapshot.get('Progress')
        snapshot_dict['start_time'] = raw_snapshot.get('StartTime')
        snapshot_dict['state'] = raw_snapshot.get('State')
        snapshot_dict['volume_id'] = raw_snapshot.get('VolumeId')
        snapshot_dict['volume_size'] = raw_snapshot.get('VolumeSize')
        snapshot_dict['create_volume_permissions'] = raw_snapshot.get('CreateVolumePermissions')
        snapshot_dict['arn'] = format_arn(self.partition, self.service, self.region, raw_snapshot.get('OwnerId'), raw_snapshot.get('SnapshotId'), self.resource_type)
        return snapshot_dict['id'], snapshot_dict

    @staticmethod
    def _is_public(snapshot):
        return any([permission.get('Group') == 'all' for permission in snapshot['CreateVolumePermissions']])
