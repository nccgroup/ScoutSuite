from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .mysql_servers import MySQLServers


class MySQLServers(Subscriptions):
    _children = [
        (MySQLServers, 'servers')
    ]