from ScoutSuite.providers.aliyun.resources.base import AliyunCompositeResources
from ScoutSuite.providers.aliyun.resources.iam.users import Users


class IAM(AliyunCompositeResources):
    _children = [
        (Users, 'users'),
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)
