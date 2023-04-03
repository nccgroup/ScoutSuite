from ScoutSuite.providers.ksyun.resources.base import KsyunResources
from ScoutSuite.providers.ksyun.facade.base import KsyunFacade


class Snapshots(KsyunResources):
    def __init__(self, facade: KsyunFacade, region: str):
        super().__init__(facade)
        self.region = region
        # self.partition = facade.partition
        # self.service = 'ec2'
        self.resource_type = 'snapshot'

    async def fetch_all(self):
        raw_snapshots = await self.facade.ebs.get_snapshots(self.region)
        for raw_snapshot in raw_snapshots:
            name, resource = self._parse_snapshot(raw_snapshot)
            self[name] = resource

    def _parse_snapshot(self, raw_snapshot):
        snapshot_dict = {}
        snapshot_dict['id'] = raw_snapshot.get('SnapshotId')
        snapshot_dict['name'] = raw_snapshot.get('SnapshotName')
        snapshot_dict['description'] = None
        snapshot_dict['public'] = raw_snapshot.get('ImageRelated')
        # snapshot_dict['encrypted'] = raw_snapshot.get('Encrypted')
        # snapshot_dict['kms_key_id'] = raw_snapshot.get('KmsKeyId')
        # snapshot_dict['owner_id'] = raw_snapshot.get('VolumeId')
        snapshot_dict['progress'] = raw_snapshot.get('Progress')
        snapshot_dict['start_time'] = raw_snapshot.get('CreateTime')
        snapshot_dict['state'] = raw_snapshot.get('SnapshotStatus')
        snapshot_dict['volume_id'] = raw_snapshot.get('VolumeId')
        snapshot_dict['volume_size'] = raw_snapshot.get('Size')
        # snapshot_dict['create_volume_permissions'] = raw_snapshot.get('CreateVolumePermissions')
        # snapshot_dict['arn'] = format_arn(self.partition, self.service, self.region, raw_snapshot.get('OwnerId'),
        #                                   raw_snapshot.get('SnapshotId'), self.resource_type)
        return snapshot_dict['id'], snapshot_dict

    @staticmethod
    def _is_public(snapshot):
        return any([permission.get('Group') == 'all' for permission in snapshot['CreateVolumePermissions']])
