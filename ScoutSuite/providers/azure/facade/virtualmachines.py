from azure.mgmt.compute import ComputeManagementClient

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently


class VirtualMachineFacade:
    def __init__(self, credentials, subscription_id):
        self._client = ComputeManagementClient(credentials, subscription_id, base_url=credentials.cloud_environment.endpoints.resource_manager)

    async def get_instances(self):
        try:
            return await run_concurrently(
                lambda: list(self._client.virtual_machines.list_all())
            )
        except Exception as e:
            print_exception('Failed to retrieve virtual machines: {}'.format(e))
            return []
