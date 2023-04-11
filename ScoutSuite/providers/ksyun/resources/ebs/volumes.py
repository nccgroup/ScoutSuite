from ScoutSuite.providers.ksyun.resources.base import KsyunResources
from ScoutSuite.providers.ksyun.facade.base import KsyunFacade


class Volumes(KsyunResources):
    def __init__(self, facade: KsyunFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_volumes = await self.facade.ebs.get_volumes(region=self.region)
        if raw_volumes:
            for raw_volume in raw_volumes:
                name, resource = await self._parse_volume(raw_volume)
                self[name] = resource

    async def _parse_volume(self, raw_volume):

        volume_dict = {}

        volume_dict['id'] = raw_volume.get('VolumeId')
        volume_dict['name'] = raw_volume.get('VolumeName')
        volume_dict['arn'] = raw_volume.get('InstanceId')


        return volume_dict['id'], volume_dict
