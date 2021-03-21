from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureCompositeResources
from ScoutSuite.providers.azure.utils import get_resource_group_name
from ScoutSuite.providers.utils import get_non_provider_id

from .configuration_connection_throttling import ConfigurationConnectionThrottling

from .configuration_log_checkpoints import ConfigurationLogCheckpoints
from .configuration_log_connections import ConfigurationLogConnections
from .configuration_log_disconnections import ConfigurationLogDisconnections
from .configuration_log_duration import ConfigurationLogDuration
from .configuration_log_retention_days import ConfigurationLogRetentionDays
from .posgresql_firewall_rules import PostgreSQLFirewallRules




class PostgreSQLServers(AzureCompositeResources):
    _children = [
        (ConfigurationLogCheckpoints, 'log_checkpoints'),
        (ConfigurationLogConnections, 'log_connections'),
        (ConfigurationLogDisconnections, 'log_disconnections'),
        (ConfigurationLogDuration, 'log_duration'),
        (ConfigurationConnectionThrottling, 'connection_throttling'),
        (ConfigurationLogRetentionDays, 'log_retention_days'),
        (PostgreSQLFirewallRules, 'postgresql_firewall_rules'),
        (ConfigurationLogRetentionDays, 'log_retention_days')
    ]

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_server in await self.facade.postgresqldatabase.get_servers(self.subscription_id):
            id, server = self._parse_server(raw_server)
            self[id] = server

        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={server_id: {'resource_group_name': server['resource_group_name'],
                                'server_name': server['name'],
                                'subscription_id': self.subscription_id}
                    for (server_id, server) in self.items()}
        )

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
