from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.azure.facade.base import AzureFacade


class ReplicationLinks(Resources):

    def __init__(self, resource_group_name, server_name, database_name, facade: AzureFacade):
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name
        self.facade = facade

    async def fetch_all(self):
        links = await self.facade.sqldatabase.get_database_replication_links(
            self.resource_group_name, self.server_name, self.database_name)
        self._parse_links(links)

    def _parse_links(self, links):
        self.update({
            'replication_configured': len(links) > 0
        })
