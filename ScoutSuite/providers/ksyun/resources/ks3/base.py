from ScoutSuite.providers.ksyun.resources.base import KsyunCompositeResources
from ScoutSuite.providers.ksyun.resources.ks3.buckets import Buckets


class KS3(KsyunCompositeResources):
    _children = [
        (Buckets, 'buckets')
    ]

    async def fetch_all(self, **kwargs):
        await self._fetch_children(resource_parent=self)
