from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class BlobServices(AzureResources):

    def __init__(self, facade: AzureFacade, resource_group_name: str, storage_account_name: str, subscription_id: str):
        super().__init__(facade)
        self.resource_group_name = resource_group_name
        self.storage_account_name = storage_account_name
        self.subscription_id = subscription_id

    async def fetch_all(self):
        raw_blob_services = await self.facade.storageaccounts.get_blob_services(self.resource_group_name,
                                                                                    self.storage_account_name,
                                                                                    self.subscription_id)
        for raw_blob_service in raw_blob_services:
            id, blob_service = self._parse_blob_service(raw_blob_service)
            self[id] = blob_service

    def _parse_blob_service(self, raw_blob_service):
        blob_service = {}
        blob_service['id'] = get_non_provider_id(raw_blob_service.id.lower())
        blob_service['name'] = raw_blob_service.name
        blob_service['soft_delete_enabled'] = raw_blob_service.delete_retention_policy.enabled

        return blob_service['id'], blob_service
