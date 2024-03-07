from azure.mgmt.keyvault import KeyVaultManagementClient

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import map_concurrently, run_concurrently
from ScoutSuite.utils import get_user_agent


class KeyVaultFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        client = KeyVaultManagementClient(self.credentials.get_credentials(),
                                          subscription_id=subscription_id, user_agent=get_user_agent())
        return client

    async def get_key_vaults(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.vaults.list_by_subscription()))
        except Exception as e:
            print_exception(f'Failed to retrieve key vaults: {e}')
            return []

    async def get_keys(self, subscription_id: str, resourcegroup_name: str, keyvault_name: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.keys.list(resource_group_name=resourcegroup_name, vault_name=keyvault_name)))
        except Exception as e:
            print_exception(f'Failed to retrieve keys from key vault {keyvault_name}: {e}')
            return []
        
    async def get_detailed_keys(self, subscription_id: str, resourcegroup_name: str, keyvault_name: str, key_names: list[str]):
        try:
            return await map_concurrently(self.get_key, key_names, subscription_id=subscription_id, resourcegroup_name=resourcegroup_name, keyvault_name=keyvault_name)
        except Exception as e:
            print_exception(f'Failed to retrieve keys from key vault {keyvault_name}: {e}')
            return []        
        
    async def get_key(self, key_name: str, subscription_id: str, resourcegroup_name: str, keyvault_name: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: client.keys.get(resource_group_name=resourcegroup_name, vault_name=keyvault_name, key_name=key_name))
        except Exception as e:
            print_exception(f'Failed to retrieve key {key_name}: {e}')
            return None
        
    async def get_secrets(self, subscription_id: str, resourcegroup_name: str, keyvault_name: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.secrets.list(resource_group_name=resourcegroup_name, vault_name=keyvault_name)))
        except Exception as e:
            print_exception(f'Failed to retrieve secrets from key vault {keyvault_name}: {e}')
            return []
