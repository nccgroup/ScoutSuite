from ScoutSuite.providers.base.configs.resources import Resources


class Pricings(Resources):

    def __init__(self, facade):
        self.facade = facade

    async def fetch_all(self):
        for raw_pricing in await self.facade.get_pricings():
            id, pricing = self._parse(raw_pricing)
            self[id] = pricing

    def _parse(self, pricing):
        pricing_dict = {}
        pricing_dict['id'] = pricing.id
        pricing_dict['name'] = pricing.name
        pricing_dict['pricing_tier'] = pricing.pricing_tier

        return pricing_dict['id'], pricing_dict
