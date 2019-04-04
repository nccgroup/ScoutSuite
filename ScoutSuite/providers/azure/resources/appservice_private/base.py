from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.azure.facade.appservice_private import AppServiceFacade
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.providers.azure.facade.base import AzureFacade


class WebApplications(Resources):

    def __init__(self, facade: AzureFacade):
        self.facade = facade

    async def fetch_all(self, credentials, **kwargs):
        self['web_apps'] = {}
        # The following loop could be parallelized in case of bottleneck:
        for raw_web_app in await self.facade.appservice.get_web_apps():
            id, web_app = self._parse_web_app(raw_web_app)
            self['web_apps'][id] = web_app

        self['web_apps_count'] = len(self['web_apps'])

    def _parse_web_app(self, web_app):
        web_app_dict = {}
        web_app_dict['id'] = get_non_provider_id(web_app.id)
        web_app_dict['name'] = web_app.name
        web_app_dict['http_allowed'] = not web_app.https_only
        web_app_dict['tls_v1_supported'] = web_app.config.min_tls_version == "1.0"

        return web_app_dict['id'], web_app_dict
