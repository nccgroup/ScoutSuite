from ScoutSuite.providers.aliyun.resources.base import AliyunCompositeResources
from ScoutSuite.providers.aliyun.resources.vpc.vpcs import VPCs


class VPC(AliyunCompositeResources):
    _children = [
        (VPCs, 'vpcs')
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)
