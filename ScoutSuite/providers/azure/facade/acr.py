from azure.mgmt.containerregistry import ContainerRegistryManagementClient

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.utils import get_user_agent


class ACRFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        client = ContainerRegistryManagementClient(self.credentials.get_credentials(),
                                         subscription_id=subscription_id, user_agent=get_user_agent())
        return client

    async def get_registries(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            registries  = await run_concurrently(
                lambda: list(client.registries.list())
            )
        except Exception as e:
            print_exception(f'Failed to retrieve container registries: {e}')
            return []
        else:
            return registries
