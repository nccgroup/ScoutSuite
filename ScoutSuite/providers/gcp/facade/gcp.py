from ScoutSuite.providers.gcp.facade.base import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.cloudsql import CloudSQLFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils

class GCPFacade(GCPBaseFacade):
    def __init__(self):
        super(GCPFacade, self).__init__('cloudresourcemanager', 'v1')
        self.cloudsql = CloudSQLFacade()

    async def get_projects(self):
        resourcemanager_client = self._get_client()
        request = resourcemanager_client.projects().list() 
        projects_group = resourcemanager_client.projects()
        return await GCPFacadeUtils.get_all('projects', request, projects_group)