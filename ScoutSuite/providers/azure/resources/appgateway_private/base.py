from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.utils import get_non_provider_id


class ApplicationGateways(Resources):
    def __init__(self, facade: AzureFacade):
        self.facade = facade

    async def fetch_all(self, credentials, **kwargs):
        self['app_gateways'] = {}
        for raw_app_gateway in await self.facade.appgateway.get_application_gateways():
            id, app_gateway = self._parse_app_gateway(raw_app_gateway)
            self['app_gateways']['id'] = app_gateway

        self['app_gateways_count'] = len(self['app_gateways'])

    def _parse_app_gateway(self, app_gateway):
        app_gateway_dict = {}
        app_gateway_dict['id'] = get_non_provider_id(app_gateway.id)
        app_gateway_dict['name'] = app_gateway.name
        app_gateway_dict['web_app_firewall_enabled'] = self._is_web_app_firewall_enabled(app_gateway)

        return app_gateway_dict['id'], app_gateway_dict

    def _is_web_app_firewall_enabled(self, app_gateway):
        if app_gateway.web_application_firewall_configuration is None:
            return False

        return app_gateway.web_application_firewall_configuration.enabled
