from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.core.console import print_exception


class Pricings(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        parsing_error_counter = 0
        for raw_pricing in await self.facade.securitycenter.get_pricings(self.subscription_id):
            try:
                id, pricing = self._parse_pricing(raw_pricing)
                self[id] = pricing
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_pricing(self, pricing):
        pricing_dict = {}
        pricing_dict['id'] = pricing.id
        pricing_dict['name'] = pricing.name
        pricing_dict['pricing_tier'] = pricing.pricing_tier

        return pricing_dict['id'], pricing_dict
