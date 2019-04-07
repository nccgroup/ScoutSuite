from ScoutSuite.providers.azure.resources.base import AzureResources


class BlobContainers(AzureResources):
    async def fetch_all(self):
        raw_blob_containers = await self.facade.storageaccounts.get_blob_containers(
            self.scope['resource_group_name'], self.scope['storage_account_name']
        )
        for raw_blob_container in raw_blob_containers:
            id, blob_container = self._parse_blob_container(raw_blob_container)
            self[id] = blob_container

    def _parse_blob_container(self, raw_blob_container):
        blob_container = {}
        blob_container['id'] = raw_blob_container.name
        blob_container['public_access_allowed'] = raw_blob_container.public_access != "None"

        return blob_container['id'], blob_container
