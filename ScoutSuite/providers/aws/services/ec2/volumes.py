from ScoutSuite.providers.aws.resources.resources import AWSSimpleResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade
from ScoutSuite.providers.aws.aws import get_name


class Volumes(AWSSimpleResources):
    async def get_resources_from_api(self):
        return self.facade.ec2.get_volumes(self.scope['region'])

    def parse_resource(self, raw_volume):
        raw_volume['id'] = raw_volume.pop('VolumeId')
        raw_volume['name'] = get_name(raw_volume, raw_volume, 'id')
        return raw_volume['id'], raw_volume
