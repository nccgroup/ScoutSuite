from ScoutSuite.providers.azure.resources.base import AzureResources


class VirtualNetworks(AzureResources):
    async def fetch_all(self):
        for raw_virtual_network in await self.facade.network.get_virtual_networks():
            id, virtual_network = self._parse_virtual_network(raw_virtual_network)
            self[id] = virtual_network

    def _parse_virtual_network(self, virtual_network):
        pass
