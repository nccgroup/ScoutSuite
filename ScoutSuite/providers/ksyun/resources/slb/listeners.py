from ScoutSuite.providers.ksyun.resources.base import KsyunResources
from ScoutSuite.providers.ksyun.facade.base import KsyunFacade


class Listeners(KsyunResources):
    def __init__(self, facade: KsyunFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_listeners = await self.facade.slb.get_listeners(region=self.region)
        if raw_listeners:
            for raw_listener in raw_listeners:
                id, listener = await self._parse_listener(raw_listener)
                self[id] = listener

    async def _parse_listener(self, raw_listener):

        listener_dict = {}

        # listener_dict['id'] = raw_listener.get('InstanceId')

        return listener_dict['id'], listener_dict
