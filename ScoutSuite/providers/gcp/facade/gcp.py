from googleapiclient import discovery
from ScoutSuite.providers.gcp.utils import MemoryCache
from ScoutSuite.providers.gcp.facade.facade import Facade
from ScoutSuite.providers.gcp.facade.iam import IAMFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils

class GCPFacade(Facade):
    def __init__(self):
        super(GCPFacade, self).__init__()
        self.iam = IAMFacade()

    def _build_client(self):
        return discovery.build('cloudresourcemanager', 'v1', cache_discovery=False, cache=MemoryCache())

    # TODO: Make truly async    
    async def get_projects(self):
        resourcemanager_client = self._get_client()
        request = resourcemanager_client.projects().list() 
        projects_group = resourcemanager_client.projects()
        return await GCPFacadeUtils.get_all('projects', request, projects_group)