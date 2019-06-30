from ScoutSuite.providers.aliyun.resources.base import AliyunResources
from ScoutSuite.providers.aliyun.facade.base import AliyunFacade


class Instances(AliyunResources):
    def __init__(self, facade: AliyunFacade, region: str):
        super(Instances, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        for raw_instance in await self.facade.ecs.get_instances(region=self.region):
            id, instance = await self._parse_instance(raw_instance)
            self[id] = instance

    async def _parse_instance(self, raw_instance):
        instance = {}
        instance['id'] = raw_instance['SerialNumber']

        return instance['id'], instance
