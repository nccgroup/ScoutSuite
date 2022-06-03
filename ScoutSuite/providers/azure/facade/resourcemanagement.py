from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.core.console import print_exception
from ScoutSuite.utils import get_user_agent
from azure.mgmt.resource import ResourceManagementClient


class ResourceManagementFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        client = ResourceManagementClient(self.credentials.get_credentials(),
                                          subscription_id=subscription_id,
                                          user_agent=get_user_agent())
        return client

    async def get_specific_type_resources_with_filter(self, subscription_id: str, resource_type_filter: str):
        try:
            type_filter = " and ".join([
                f'resourceType eq \'{resource_type_filter}\''
            ])
            client = self.get_client(subscription_id)
            resource = await run_concurrently(
                lambda: list(client.resources.list(filter=type_filter))
            )
            return resource
        except Exception as e:
            print_exception(f'Failed to retrieve key vault resources: {e}')
            return []

    async def get_all_resources(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            resource = await run_concurrently(
                lambda: list(client.resources.list())
            )
            return resource
        except Exception as e:
            print_exception(f'Failed to retrieve resources: {e}')
            return []
