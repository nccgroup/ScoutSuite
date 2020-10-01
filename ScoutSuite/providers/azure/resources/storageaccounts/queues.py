from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class Queues(AzureResources):

    def __init__(self, facade: AzureFacade, resource_group_name: str, storage_account_name: str, subscription_id: str):
        super().__init__(facade)
        self.resource_group_name = resource_group_name
        self.storage_account_name = storage_account_name
        self.subscription_id = subscription_id

    async def fetch_all(self):
        raw_queues = await self.facade.storageaccounts.get_queues(self.resource_group_name,
                                                                  self.storage_account_name,
                                                                  self.subscription_id)
        for raw_queue in raw_queues:
            id, queue = self._parse_queue(raw_queue)
            self[id] = queue

    def _parse_queue(self, raw_queue):
        pass
