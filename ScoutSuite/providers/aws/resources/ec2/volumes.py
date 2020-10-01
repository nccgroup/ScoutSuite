from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.utils import get_name


class Volumes(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_volumes = await self.facade.ec2.get_volumes(self.region)
        for raw_volume in raw_volumes:
            name, resource = self._parse_volume(raw_volume)
            self[name] = resource

    def _parse_volume(self, raw_volume):
        raw_volume['id'] = raw_volume.pop('VolumeId')
        raw_volume['name'] = get_name(raw_volume, raw_volume, 'id')
        raw_volume['arn'] = 'arn:aws:ec2:{}:{}:volume/{}'.format(self.region,
                                                                             self.facade.owner_id,
                                                                             raw_volume.get('name'))
        if "Tags" in raw_snapshot:
            raw_snapshot['tags'] = {x["Key"]: x["Value"] for x in raw_snapshot["Tags"]}
        return raw_volume['id'], raw_volume
