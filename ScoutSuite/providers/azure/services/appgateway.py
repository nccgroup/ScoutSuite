# -*- coding: utf-8 -*-

from ScoutSuite.providers.azure.configs.base import AzureBaseConfig


class AppGatewayConfig(AzureBaseConfig):
    targets = (
        ('application_gateways', 'Application Gateways', 'list_all', {}, False),
    )

    def __init__(self, thread_config):

        self.app_gateways = {}
        self.app_gateways_count = 0

        super(AppGatewayConfig, self).__init__(thread_config)

    def parse_application_gateways(self, app_gateway, params):
        app_gateway_dict = {}
        app_gateway_dict['id'] = self.get_non_provider_id(app_gateway.id)
        app_gateway_dict['name'] = app_gateway.name
        app_gateway_dict['web_app_firewall_enabled'] = self._is_web_app_firewall_enabled(app_gateway)

        self.app_gateways[app_gateway_dict['id']] = app_gateway_dict

    def _is_web_app_firewall_enabled(self, app_gateway):
        if app_gateway.web_application_firewall_configuration is None:
            return False

        return app_gateway.web_application_firewall_configuration.enabled
