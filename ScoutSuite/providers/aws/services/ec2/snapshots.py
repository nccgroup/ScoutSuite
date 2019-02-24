from ScoutSuite.providers.aws.configs.regions_config import ScopedResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade
from opinel.utils.aws import get_name


class Snapshots(ScopedResources):

    # TODO: The init could take a "scope" dictionary containing the necessary info. In this case, the owner_id and the region
    def __init__(self, owner_id):
        self.owner_id = owner_id
        self.facade = AWSFacade()

    async def get_resources_in_scope(self, region):
        return self.facade.ec2.get_snapshots(region, self.owner_id)

    def parse_resource(self, raw_snapshot):
        raw_snapshot['id'] = raw_snapshot.pop('SnapshotId')
        raw_snapshot['name'] = get_name(raw_snapshot, raw_snapshot, 'id')
        raw_snapshot['public'] = self._is_public(raw_snapshot)
        return raw_snapshot['id'], raw_snapshot

    @staticmethod
    def _is_public(snapshot):
        return any([permission.get('Group') == 'all' for permission in snapshot['CreateVolumePermissions']])
