from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .web_apps import WebApplication


class AppServices(Subscriptions):
    _children = [
        (WebApplication, 'web_apps')
    ]
