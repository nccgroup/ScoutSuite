from ScoutSuite.providers.aliyun.resources.base import AliyunCompositeResources
from ScoutSuite.providers.aliyun.resources.kms.keys import Keys


class KMS(AliyunCompositeResources):
    _children = [
        (Keys, 'keys')
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)
