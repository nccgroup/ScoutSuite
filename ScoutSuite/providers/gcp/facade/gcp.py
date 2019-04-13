import logging
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.base import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.cloudresourcemanager import CloudResourceManagerFacade
from ScoutSuite.providers.gcp.facade.cloudsql import CloudSQLFacade
from ScoutSuite.providers.gcp.facade.cloudstorage import CloudStorageFacade
from ScoutSuite.providers.gcp.facade.gce import GCEFacade
from ScoutSuite.providers.gcp.facade.iam import IAMFacade
from ScoutSuite.providers.gcp.facade.stackdriverlogging import StackdriverLoggingFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils

# Try to import proprietary facades
try:
    from ScoutSuite.providers.gcp.facade.gke_private import GKEFacade
except ImportError:
    pass

class GCPFacade(GCPBaseFacade):
    def __init__(self):
        super(GCPFacade, self).__init__('cloudresourcemanager', 'v1')
        self.cloudresourcemanager = CloudResourceManagerFacade()
        self.cloudsql = CloudSQLFacade()
        self.cloudstorage = CloudStorageFacade()
        self.gce = GCEFacade()
        self.iam = IAMFacade()
        self.stackdriverlogging = StackdriverLoggingFacade()
        try:
            self.gke = GKEFacade(self.gce)
        except NameError as _:
            pass

        # Set logging level to error for GCP services as otherwise generates a lot of warnings
        logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
        logging.getLogger().setLevel(logging.ERROR)

    async def get_projects(self):
        try:
            resourcemanager_client = self._get_client()
            request = resourcemanager_client.projects().list() 
            projects_group = resourcemanager_client.projects()
            return await GCPFacadeUtils.get_all('projects', request, projects_group)
        except Exception as e:
            print_exception('Failed to retrieve projects: {}'.format(e))
            return []