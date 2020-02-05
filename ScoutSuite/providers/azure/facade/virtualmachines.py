from azure.mgmt.compute import ComputeManagementClient

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently


class VirtualMachineFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        return ComputeManagementClient(self.credentials.arm_credentials, subscription_id=subscription_id)

    async def get_instances(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.virtual_machines.list_all())
            )
        except Exception as e:
            print_exception('Failed to retrieve virtual machines: {}'.format(e))
            return []
