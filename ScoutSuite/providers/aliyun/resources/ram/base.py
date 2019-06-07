from ScoutSuite.providers.aliyun.resources.base import AliyunCompositeResources
from ScoutSuite.providers.aliyun.resources.ram.users import Users


class RAM(AliyunCompositeResources):
    _children = [
        (Users, 'users'),
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)

        # TODO for each user check last login & API key usage for "last activity"
