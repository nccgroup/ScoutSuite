from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class Pricings(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super(Pricings, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_pricing in await self.facade.securitycenter.get_pricings(self.subscription_id):
            id, pricing = self._parse_pricing(raw_pricing)
            self[id] = pricing

    def _parse_pricing(self, pricing):
        pricing_dict = {}
        pricing_dict['id'] = pricing.id
        pricing_dict['name'] = pricing.name
        pricing_dict['pricing_tier'] = pricing.pricing_tier

        return pricing_dict['id'], pricing_dict
