from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.core.console import print_exception


class BlobContainers(AzureResources):

    def __init__(self, facade: AzureFacade, resource_group_name: str, storage_account_name: str, subscription_id: str):
        super().__init__(facade)
        self.resource_group_name = resource_group_name
        self.storage_account_name = storage_account_name
        self.subscription_id = subscription_id

    async def fetch_all(self):
        raw_blob_containers = await self.facade.storageaccounts.get_blob_containers(self.resource_group_name,
                                                                                    self.storage_account_name,
                                                                                    self.subscription_id)
        for raw_blob_container in raw_blob_containers:
            try:
                id, blob_container = self._parse_blob_container(raw_blob_container)
                self[id] = blob_container
            except Exception as e:
                print_exception('Failed to parse {} resource: {}'.format(self.__class__.__name__, e))

    def _parse_blob_container(self, raw_blob_container):
        blob_container = {}
        blob_container['id'] = raw_blob_container.name
        blob_container['public_access_allowed'] = raw_blob_container.public_access != "None"

        return blob_container['id'], blob_container
