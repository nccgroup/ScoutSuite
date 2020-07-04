from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .vaults import Vaults


class KeyVaults(Subscriptions):
    _children = [
        (Vaults, 'vaults')
    ]
