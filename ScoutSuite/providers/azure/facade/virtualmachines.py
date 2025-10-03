from azure.mgmt.compute import ComputeManagementClient
import asyncio

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.utils import get_user_agent


class VirtualMachineFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):

        client = ComputeManagementClient(self.credentials.get_credentials(),
                                         subscription_id=subscription_id,
                                         user_agent=get_user_agent())
        return client

    async def get_instances(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            try:
                return await run_concurrently(
                    lambda: list(client.virtual_machines.list_all())
                )
            except AttributeError as ae:
                if 'throttler' in str(ae):
                    loop = asyncio.get_event_loop()
                    return await loop.run_in_executor(
                        None, lambda: list(client.virtual_machines.list_all())
                    )
                else:
                    raise
        except Exception as e:
            print_exception(f'Failed to retrieve virtual machines: {e}')
            return []

    async def get_instance_extensions(self, subscription_id: str,
                                      instance_name: str,
                                      resource_group: str):
        try:
            client = self.get_client(subscription_id)
            try:
                extensions = await run_concurrently(
                    lambda: client.virtual_machine_extensions.list(resource_group,
                                                                   instance_name)
                )
            except AttributeError as ae:
                if 'throttler' in str(ae):
                    loop = asyncio.get_event_loop()
                    extensions = await loop.run_in_executor(
                        None, lambda: client.virtual_machine_extensions.list(resource_group, instance_name)
                    )
                else:
                    raise
            return list(extensions.value)
        except Exception as e:
            print_exception(f'Failed to retrieve virtual machine extensions: {e}')
            return []

    async def get_disks(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            try:
                return await run_concurrently(
                    lambda: list(client.disks.list())
                )
            except AttributeError as ae:
                if 'throttler' in str(ae):
                    loop = asyncio.get_event_loop()
                    return await loop.run_in_executor(
                        None, lambda: list(client.disks.list())
                    )
                else:
                    raise
        except Exception as e:
            print_exception(f'Failed to retrieve disks: {e}')
            return []

    async def get_snapshots(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            try:
                return await run_concurrently(
                    lambda: list(client.snapshots.list())
                )
            except AttributeError as ae:
                if 'throttler' in str(ae):
                    loop = asyncio.get_event_loop()
                    return await loop.run_in_executor(
                        None, lambda: list(client.snapshots.list())
                    )
                else:
                    raise
        except Exception as e:
            print_exception(f'Failed to retrieve snapshots: {e}')
            return []

    async def get_images(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            try:
                return await run_concurrently(
                    lambda: list(client.images.list())
                )
            except AttributeError as ae:
                if 'throttler' in str(ae):
                    loop = asyncio.get_event_loop()
                    return await loop.run_in_executor(
                        None, lambda: list(client.images.list())
                    )
                else:
                    raise
        except Exception as e:
            print_exception(f'Failed to retrieve images: {e}')
            return []
