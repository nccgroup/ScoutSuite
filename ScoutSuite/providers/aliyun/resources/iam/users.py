from ScoutSuite.providers.aliyun.resources.base import AliyunCompositeResources

from .api_keys import ApiKeys


class Users(AliyunCompositeResources):
    _children = [
        (ApiKeys, 'api_keys')
    ]

    async def fetch_all(self):
        for raw_user in await self.facade.iam.get_users():
            id, user = self._parse_user(raw_user)
            self[id] = user

        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={user_id: {'user': user}
                    for user_id, user in self.items()}
        )

    def _parse_user(self, raw_user):
        user = {}
        user['id'] = raw_user['UserId']
        user['name'] = raw_user['UserName']

        return user['id'], user
