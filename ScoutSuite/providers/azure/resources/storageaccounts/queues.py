from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.core.console import print_exception


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
        parsing_error_counter = 0
        for raw_queue in raw_queues:
            try:
                id, queue = self._parse_queue(raw_queue)
                self[id] = queue
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_queue(self, raw_queue):
        pass
