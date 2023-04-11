from ScoutSuite.providers.ksyun.resources.base import KsyunCompositeResources
from ScoutSuite.providers.ksyun.resources.actiontrail.trails import Trails


class ActionTrail(KsyunCompositeResources):
    _children = [
        (Trails, 'trails')
    ]

    async def fetch_all(self, **kwargs):
        await self._fetch_children(resource_parent=self)
