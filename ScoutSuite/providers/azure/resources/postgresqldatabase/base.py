from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .postgresql_servers import PostgreSQLServers


class PostgreSQLServers(Subscriptions):
    _children = [
        (PostgreSQLServers, 'servers')
    ]