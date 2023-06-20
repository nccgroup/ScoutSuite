from azure.mgmt.compute import ComputeManagementClient

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.utils import get_user_agent


class VirtualMachineFacade:

    def __init__(self, credentials, resource_group=None):
        self.credentials = credentials
        self.resource_group = resource_group

    def get_client(self, subscription_id: str):

        client = ComputeManagementClient(self.credentials.get_credentials(),
                                         subscription_id=subscription_id,
                                         user_agent=get_user_agent())
        return client

    async def get_instances(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            if self.resource_group:
                return await run_concurrently(
                    lambda: list(client.virtual_machines.list(resource_group_name=self.resource_group))
                )
            else:
                return await run_concurrently(
                    lambda: list(client.virtual_machines.list_all())
                )
        except Exception as e:
            print_exception(f'Failed to retrieve virtual machines: {e}')
            return []

    async def get_instance_extensions(self, subscription_id: str,
                                      instance_name: str,
                                      resource_group: str):
        try:
            client = self.get_client(subscription_id)
            extensions = await run_concurrently(
                lambda: client.virtual_machine_extensions.list(resource_group,
                                                               instance_name)
            )
            return list(extensions.value)
        except Exception as e:
            print_exception(f'Failed to retrieve virtual machine extensions: {e}')
            return []

    async def get_disks(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            if self.resource_group:
                return await run_concurrently(
                    lambda: list(client.disks.list_by_resource_group(self.resource_group))
                )
            else:
                return await run_concurrently(
                    lambda: list(client.disks.list())
                )
        except Exception as e:
            print_exception(f'Failed to retrieve disks: {e}')
            return []

    async def get_snapshots(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)

            if self.resource_group:
                return await run_concurrently(
                    lambda: list(client.snapshots.list_by_resource_group(self.resource_group))
                )
            else: 
                return await run_concurrently(
                    lambda: list(client.snapshots.list())
                )
        except Exception as e:
            print_exception(f'Failed to retrieve snapshots: {e}')
            return []

    async def get_images(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)

            if self.resource_group:
                return await run_concurrently(
                    lambda: list(client.images.list_by_resource_group(self.resource_group))
                )
            else:
                return await run_concurrently(
                    lambda: list(client.images.list())
                )
        except Exception as e:
            print_exception(f'Failed to retrieve images: {e}')
            return []
