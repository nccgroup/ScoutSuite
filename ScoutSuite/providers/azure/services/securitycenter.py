# -*- coding: utf-8 -*-

from ScoutSuite.providers.azure.configs.base import AzureBaseConfig


class SecurityCenterConfig(AzureBaseConfig):
    targets = (
        ('pricings', 'Pricings', 'list', {}, False),
    )

    def __init__(self, thread_config):
        self.pricings = {}
        self.pricings_count = 0

        super(SecurityCenterConfig, self).__init__(thread_config)

    def parse_pricings(self, pricing, params):
        pricing_dict = {'id': pricing.id,
                        'name': pricing.name,
                        'pricing_tier': pricing.pricing_tier}

        self.pricings[pricing_dict['id']] = pricing_dict
