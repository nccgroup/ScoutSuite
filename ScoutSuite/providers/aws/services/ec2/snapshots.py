from ScoutSuite.providers.aws.configs.regions_config import ScopedResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade

class Snapshots(ScopedResources):
    def __init__(self, owner_id):
        self.owner_id = owner_id
        self.facade = AWSFacade()
    
    async def get_resources_in_scope(self, region): 
        return self.facade.ec2.get_images(region, self.owner_id)

    def parse_resource(self, raw_image):
        raw_image['id'] = raw_image['ImageId']
        raw_image['name'] = raw_image['Name']

        return raw_image['id'], raw_image


    def parse_snapshot(self, snapshot):
        snapshot['id'] = snapshot.pop('SnapshotId')
        # snapshot['name'] = get_name(snapshot, snapshot, 'id')
        # self.snapshots[snapshot['id']] = snapshot
        # # Get snapshot attribute
        # snapshot['createVolumePermission'] = \
        # api_clients[region].describe_snapshot_attribute(Attribute='createVolumePermission', SnapshotId=snapshot['id'])[
        #     'CreateVolumePermissions']
        # snapshot['public'] = self._is_public(snapshot)