from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.basefacade import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils
from ScoutSuite.providers.utils import run_concurrently

class CloudMemorystoreRedisFacade(GCPBaseFacade):
    def __init__(self):
        super().__init__('redis', 'v1beta1')

    async def get_redis_instances(self, project_id: str):
        try:
            formatted_parent = f'projects/{project_id}/locations/-'
            cloudmem_client = self._get_client()
            instances_group = cloudmem_client.projects().locations().instances()
            request = instances_group.list(parent=formatted_parent)
            return await GCPFacadeUtils.get_all('instances', request, instances_group)
        except Exception as e:
            print_exception(f'Failed to retrieve redis instances: {e}')
            return []
