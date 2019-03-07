from googleapiclient import discovery
from ScoutSuite.providers.gcp.utils import MemoryCache
from ScoutSuite.providers.gcp.facade.stackdriverlogging import StackdriverLoggingFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils

class GCPFacade:
    def __init__(self):
        self._resourcemanager_client = None
        self.stackdriverlogging = StackdriverLoggingFacade()

    def _get_resourcemanager_client(self):
        if self._resourcemanager_client is None:
            self._resourcemanager_client = discovery.build('cloudresourcemanager', 'v1', cache_discovery=False, cache=MemoryCache())
        return self._resourcemanager_client

    # TODO: Make truly async    
    async def get_projects(self):
        resourcemanager_client = self._get_resourcemanager_client()
        request = resourcemanager_client.projects().list() 
        projects_group = resourcemanager_client.projects()
        return await GCPFacadeUtils.get_all('projects', request, projects_group)

