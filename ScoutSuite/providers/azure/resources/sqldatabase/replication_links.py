from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class ReplicationLinks(AzureResources):

    def __init__(self, facade: AzureFacade, resource_group_name: str, server_name: str, database_name: str,
                 subscription_id: str):
        super().__init__(facade)
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name
        self.subscription_id = subscription_id

    async def fetch_all(self):
        links = await self.facade.sqldatabase.get_database_replication_links(
            self.resource_group_name, self.server_name, self.database_name, self.subscription_id)
        self._parse_links(links)

    def _parse_links(self, links):
        links_count = len(list(links))
        self.update({
            'replication_configured': links_count > 0
        })
