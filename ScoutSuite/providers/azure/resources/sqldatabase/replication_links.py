from ScoutSuite.providers.azure.resources.base import AzureResources


class ReplicationLinks(AzureResources):
    async def fetch_all(self):
        links = await self.facade.sqldatabase.get_database_replication_links(
            self.scope['resource_group_name'], self.scope['server_name'], self.scope['database_name'])
        self._parse_links(links)

    def _parse_links(self, links):
        self.update({
            'replication_configured': len(links) > 0
        })
