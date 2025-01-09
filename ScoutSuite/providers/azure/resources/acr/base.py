from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .registries import Registries


class ACRRegistries(Subscriptions):
    _children = [
        (Registries, 'registries')
    ]
