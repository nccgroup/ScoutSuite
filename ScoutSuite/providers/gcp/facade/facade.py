from googleapiclient import discovery
from ScoutSuite.providers.gcp.utils import MemoryCache
from ScoutSuite.providers.gcp.facade.stackdriverlogging import StackdriverLoggingFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils

class GCPFacade:
    def __init__(self):
        self._resourcemanager_client = discovery.build('cloudresourcemanager', 'v1', cache_discovery=False, cache=MemoryCache())
        self.stackdriverlogging = StackdriverLoggingFacade()

    # TODO: Make truly async    
    async def get_projects(self):
        request = self._resourcemanager_client.projects().list() 
        projects_group = self._resourcemanager_client.projects()
        return await GCPFacadeUtils.get_all('projects', request, projects_group)

