from azure.mgmt.storage import StorageManagementClient
from ScoutSuite.providers.utils import run_concurrently


class StorageAccountsFacade:
    def __init__(self, credentials, subscription_id):
        self._client = StorageManagementClient(credentials, subscription_id)

    async def get_storage_accounts(self):
        return await run_concurrently(self._client.storage_accounts.list)

    async def get_blob_containers(self, resource_group_name, storage_account_name):
        return await run_concurrently(
            lambda: self._client.blob_containers.list(resource_group_name, storage_account_name).value
        )
