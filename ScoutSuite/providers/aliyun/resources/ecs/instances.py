from ScoutSuite.providers.aliyun.resources.base import AliyunResources
from ScoutSuite.providers.aliyun.facade.base import AliyunFacade


class Instances(AliyunResources):
    def __init__(self, facade: AliyunFacade):
        super(Instances, self).__init__(facade)

    async def fetch_all(self):
        for raw_instance in await self.facade.ecs.get_instances():
            id, instance = await self._parse_instance(raw_instance)
            self[id] = instance

    async def _parse_instance(self, raw_instance):
        instance = {}
        instance['id'] = raw_instance['id']

        return instance['id'], instance
