from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.utils import get_name


class Snapshots(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(Snapshots, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_snapshots = await self.facade.ec2.get_snapshots(self.region)
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
