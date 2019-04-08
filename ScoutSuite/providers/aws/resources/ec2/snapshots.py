from ScoutSuite.providers.aws.resources.resources import AWSResources
from ScoutSuite.providers.aws.utils import get_name


class Snapshots(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_snapshots = await self.facade.ec2.get_snapshots(self.scope['region'], self.scope['owner_id'])
        for raw_snapshot in raw_snapshots:
            name, resource = self._parse_snapshot(raw_snapshot)
            self[name] = resource

    def _parse_snapshot(self, raw_snapshot):
        raw_snapshot['id'] = raw_snapshot.pop('SnapshotId')
        raw_snapshot['name'] = get_name(raw_snapshot, raw_snapshot, 'id')
        raw_snapshot['public'] = self._is_public(raw_snapshot)
        return raw_snapshot['id'], raw_snapshot

    @staticmethod
    def _is_public(snapshot):
        return any([permission.get('Group') == 'all' for permission in snapshot['CreateVolumePermissions']])
