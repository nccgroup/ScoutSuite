from ScoutSuite.providers.azure.resources.base import AzureResources


class Users(AzureResources):
    async def fetch_all(self):
        for raw_users in await self.facade.graphrbac.get_users():
            id, user = self._parse_user(raw_users)
            self[id] = user

    def _parse_user(self, raw_user):
        # TODO
        return 1,1
