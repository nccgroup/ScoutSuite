from ScoutSuite.providers.aliyun.resources.base import AliyunCompositeResources
from ScoutSuite.providers.aliyun.resources.rds.instances import Instances


class RDS(AliyunCompositeResources):
    _children = [
        (Instances, 'instances')
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)
