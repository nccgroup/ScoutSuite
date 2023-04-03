from ScoutSuite.providers.ksyun.resources.base import KsyunResources
from ScoutSuite.providers.ksyun.facade.base import KsyunFacade


class Volumes(KsyunResources):
    def __init__(self, facade: KsyunFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_volume = await self.facade.ebs.get_volume(region=self.region)
        if raw_volume:
            for raw_volume in raw_volume:
                id, volume = await self._parse_cluster(raw_volume)
                self[id] = volume

    async def _parse_cluster(self, raw_volume):

        volume_dict = {}

        volume_dict['id'] = '1'


        return volume_dict['id'], volume_dict
