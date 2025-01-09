from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .postgresqlflexible_servers import PostgreSQLFlexibleServers


class PostgreSQLFlexibleServers(Subscriptions):
    _children = [
        (PostgreSQLFlexibleServers, 'servers')
    ]