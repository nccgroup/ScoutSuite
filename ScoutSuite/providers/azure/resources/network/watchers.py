from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.providers.azure.utils import get_resource_group_name


class Watchers(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_watcher in await self.facade.network.get_network_watchers(self.subscription_id):
            id, network_watcher = self._parse_network_watcher(raw_watcher)
            self[id] = network_watcher

    def _parse_network_watcher(self, raw_watcher):
        watcher_dict = {}
        watcher_dict['id'] = get_non_provider_id(raw_watcher.id)
        watcher_dict['name'] = raw_watcher.name
        watcher_dict['type'] = raw_watcher.type
        watcher_dict['location'] = raw_watcher.location
        if raw_watcher.tags is not None:
            watcher_dict['tags'] = ["{}:{}".format(key, value) for key, value in raw_watcher.tags.items()]
        else:
            watcher_dict['tags'] = []
        watcher_dict['resource_group_name'] = get_resource_group_name(raw_watcher.id)
        watcher_dict['etag'] = raw_watcher.etag
        watcher_dict['additional_properties'] = raw_watcher.additional_properties
        watcher_dict['provisioning_state'] = raw_watcher.provisioning_state
        return watcher_dict['id'], watcher_dict
