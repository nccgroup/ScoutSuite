from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureCompositeResources
from ScoutSuite.providers.azure.utils import get_resource_group_name
from ScoutSuite.providers.utils import get_non_provider_id


class MySQLServers(AzureCompositeResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_server in await self.facade.mysqldatabase.get_servers(self.subscription_id):
            id, server = self._parse_server(raw_server)
            self[id] = server

    def _parse_server(self, raw_server):
        server = {}
        server['id'] = get_non_provider_id(raw_server.id)
        server['name'] = raw_server.name
        server['resource_group_name'] = get_resource_group_name(raw_server.id)
        server['ssl_enforcement'] = raw_server.ssl_enforcement
        if raw_server.tags is not None:
            server['tags'] = ["{}:{}".format(key, value) for key, value in raw_server.tags.items()]
        else:
            server['tags'] = []
        return server['id'], server