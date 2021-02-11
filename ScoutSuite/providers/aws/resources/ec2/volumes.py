from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.utils import get_name
from ScoutSuite.core.console import print_exception


class Volumes(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_volumes = await self.facade.ec2.get_volumes(self.region)
        parsing_error_counter = 0
        for raw_volume in raw_volumes:
            try:
                name, resource = self._parse_volume(raw_volume)
                self[name] = resource
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_volume(self, raw_volume):
        raw_volume['id'] = raw_volume.pop('VolumeId')
        raw_volume['name'] = get_name(raw_volume, raw_volume, 'id')
        raw_volume['arn'] = 'arn:aws:ec2:{}:{}:volume/{}'.format(self.region,
                                                                             self.facade.owner_id,
                                                                             raw_volume.get('name'))
        return raw_volume['id'], raw_volume
