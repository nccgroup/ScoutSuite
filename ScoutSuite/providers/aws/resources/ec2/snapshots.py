from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.utils import get_name
from ScoutSuite.core.console import print_exception


class Snapshots(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_snapshots = await self.facade.ec2.get_snapshots(self.region)
        parsing_error_counter = 0
        for raw_snapshot in raw_snapshots:
            try:
                name, resource = self._parse_snapshot(raw_snapshot)
                self[name] = resource
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_snapshot(self, raw_snapshot):
        raw_snapshot['id'] = raw_snapshot.pop('SnapshotId')
        raw_snapshot['name'] = get_name(raw_snapshot, raw_snapshot, 'id')
        raw_snapshot['public'] = self._is_public(raw_snapshot)
        raw_snapshot['arn'] = 'arn:aws:ec2:{}:{}:snapshot/{}'.format(self.get('region'),
                                                                     raw_snapshot.get('OwnerId'),
                                                                     raw_snapshot.get('name'))
        return raw_snapshot['id'], raw_snapshot

    @staticmethod
    def _is_public(snapshot):
        return any([permission.get('Group') == 'all' for permission in snapshot['CreateVolumePermissions']])
