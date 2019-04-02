from ScoutSuite.providers.gcp.facade.base import GCPBaseFacade
from ScoutSuite.providers.utils import run_concurrently

class CloudResourceManagerFacade(GCPBaseFacade):
    def __init__(self):
        super(CloudResourceManagerFacade, self).__init__('cloudresourcemanager', 'v1')

    async def get_bindings(self, project_id: str):
        cloudresourcemanager_client = self._get_client()
        response = await run_concurrently(
                lambda: cloudresourcemanager_client.projects().getIamPolicy(resource=project_id).execute()
        )
        return response.get('bindings', [])


