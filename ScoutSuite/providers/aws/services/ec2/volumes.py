from ScoutSuite.providers.aws.configs.regions_config import ScopedResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade
from opinel.utils.aws import get_name


class Volumes(ScopedResources):

    # TODO: The init could take a "scope" dictionary containing the necessary info. In this case, the owner_id and the region
    def __init__(self):
        self.facade = AWSFacade()

    async def get_resources_in_scope(self, region):
        return self.facade.ec2.get_volumes(region)

    def parse_resource(self, raw_volume):
        raw_volume['id'] = raw_volume.pop('VolumeId')
        raw_volume['name'] = get_name(raw_volume, raw_volume, 'id')
        return raw_volume['id'], raw_volume
