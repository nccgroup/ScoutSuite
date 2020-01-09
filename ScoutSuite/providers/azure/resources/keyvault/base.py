from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .vaults import KeyVaults


class KeyVaut(Subscriptions):
    _children = [
        (KeyVaults, 'vaults')
    ]
