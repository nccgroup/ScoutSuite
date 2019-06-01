from ScoutSuite.providers.aliyun.resources.base import AliyunCompositeResources
from ScoutSuite.providers.aliyun.facade.facade import AliyunFacade
from ScoutSuite.providers.aliyun.resources.utils import get_non_provider_id

from .api_keys import ApiKeys


class Users(AliyunCompositeResources):
    _children = [
        (ApiKeys, 'api_keys')
    ]

    def __init__(self, facade: AliyunFacade):
        self.facade = facade

    async def fetch_all(self, **kwargs):
        for raw_user in await self.facade.iam.get_users():
            id, user = self._parse_user(raw_user)
            self[id] = user

        await self._fetch_children_of_all_resources(
            resources=self,
            kwargs={user_id: {'user': user,
                              'facade': self.facade}
                    for user_id, user in self.items()}
        )


    def _parse_user(self, raw_user):
        user = {}
        user['id'] = raw_user['UserId']
        user['name'] = raw_user['UserName']

        return user['id'], user
