from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class ReplicationLinks(AzureResources):
    def __init__(self, facade: AzureFacade, resource_group_name: str, server_name: str, database_name: str):
        super(ReplicationLinks, self).__init__(facade)
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name

    async def fetch_all(self):
        links = await self.facade.sqldatabase.get_database_replication_links(
            self.resource_group_name, self.server_name, self.database_name)
        self._parse_links(links)

    def _parse_links(self, links):
        self.update({
            'replication_configured': len(links) > 0
        })
