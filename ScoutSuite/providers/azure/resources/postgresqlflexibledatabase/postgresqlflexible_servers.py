from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureCompositeResources
from ScoutSuite.providers.azure.utils import get_resource_group_name
from ScoutSuite.providers.utils import get_non_provider_id

class PostgreSQLFlexibleServers(AzureCompositeResources):
    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_server in await self.facade.postgresqlflexibledatabase.get_servers(self.subscription_id):
            id, server = self._parse_server(raw_server)
            self[id] = server

    def _parse_server(self, raw_server):
        server = {}
        server['id'] = get_non_provider_id(raw_server.id)
        server['name'] = raw_server.name
        server['resource_group_name'] = get_resource_group_name(raw_server.id)

        server['network'] = {}
        server['network']['public_network_access'] = raw_server.network.public_network_access
        if raw_server.network.delegated_subnet_resource_id != None:
            server['network']['private_subnet'] = True
            server['network']['delegated_subnet'] = get_non_provider_id(raw_server.network.delegated_subnet_resource_id)
        else:
            server['network']['private_subnet'] = False
            server['network']['delegated_subnet'] = None

        server['auth_config'] = {}
        server['auth_config']['active_directory_auth'] = raw_server.auth_config.active_directory_auth
        server['auth_config']['password_auth'] = raw_server.auth_config.password_auth

        if raw_server.tags is not None:
            server['tags'] = ["{}:{}".format(key, value) for key, value in raw_server.tags.items()]
        else:
            server['tags'] = []
        return server['id'], server
