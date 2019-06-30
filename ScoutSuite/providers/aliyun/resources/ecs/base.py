from ScoutSuite.providers.aliyun.facade.base import AliyunFacade
from ScoutSuite.providers.aliyun.resources.regions import Regions
from ScoutSuite.providers.aliyun.resources.ecs.instances import Instances


class ECS(Regions):
    _children = [
        (Instances, 'instances')
    ]

    def __init__(self, facade: AliyunFacade):
        super(ECS, self).__init__('ecs', facade)

    async def fetch_all(self, regions):
        # await self._fetch_children(resource_parent=self, region=region)
        await super(ECS, self).fetch_all(regions)
