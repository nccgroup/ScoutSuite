from ScoutSuite.providers.aliyun.resources.base import AliyunCompositeResources
from ScoutSuite.providers.aliyun.resources.actiontrail.trails import Trails


class ActionTrail(AliyunCompositeResources):
    _children = [
        (Trails, 'trails')
    ]

    async def fetch_all(self, **kwargs):
        await self._fetch_children(resource_parent=self)
