from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .servers import Servers


class Servers(Subscriptions):
    _children = [
        (Servers, 'servers')
    ]
