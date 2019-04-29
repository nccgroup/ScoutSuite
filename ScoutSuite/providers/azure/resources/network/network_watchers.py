from ScoutSuite.providers.azure.resources.base import AzureResources


class NetworkWatchers(AzureResources):
    async def fetch_all(self):
        for raw_watcher in await self.facade.network.get_network_watchers():
            id, network_watcher = self._parse_network_watcher(raw_watcher)
            self[id] = network_watcher

    def _parse_network_watcher(self, network_watcher):
        network_watcher_dict = {}
        network_watcher_dict['id'] = network_watcher.id
        network_watcher_dict['name'] = network_watcher.name
        network_watcher_dict['provisioning_state'] = network_watcher.provisioning_state
        network_watcher_dict['location'] = network_watcher.location
        network_watcher_dict['etag'] = network_watcher.etag

        return network_watcher_dict['id'], network_watcher_dict
