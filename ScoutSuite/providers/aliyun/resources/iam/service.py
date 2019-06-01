from ScoutSuite.providers.aliyun.resources.base import AliyunCompositeResources
from ScoutSuite.providers.aliyun.resources.iam.users import Users



class IAM(AliyunCompositeResources):
    _children = [
        (Users, 'users'),
    ]

    def __init__(self, facade: AliyunCompositeResources):
        self.facade = facade
        self.service = 'iam'

    async def fetch_all(self, credentials):

        await self._fetch_children(resource_parent=self, facade=self.facade)
