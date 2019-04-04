from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.providers.gcp.facade.gcp import GCPFacade
from ScoutSuite.providers.gcp.resources.cloudresourcemanager.service import CloudResourceManager
from ScoutSuite.providers.gcp.resources.cloudsql.service import CloudSQL
from ScoutSuite.providers.gcp.resources.iam.service import IAM
from ScoutSuite.providers.gcp.resources.stackdriverlogging.service import StackdriverLogging
from ScoutSuite.providers.gcp.services.cloudstorage import CloudStorageConfig
from ScoutSuite.providers.gcp.services.computeengine import ComputeEngineConfig

# Try to import proprietary services
try:
    from ScoutSuite.providers.gcp.services.kubernetesengine_private import KubernetesEngineConfig
except ImportError:
    pass


class GCPServicesConfig(BaseServicesConfig):

    def __init__(self, credentials=None, thread_config=4, projects=None, **kwargs):
        super(GCPServicesConfig, self).__init__(credentials)

        projects = [] if projects is None else projects

        gcp_facade = GCPFacade()

        self.cloudresourcemanager = CloudResourceManager(gcp_facade)
        self.cloudstorage = CloudStorageConfig(thread_config=thread_config)
        self.cloudsql = CloudSQL(gcp_facade)
        self.computeengine = ComputeEngineConfig(thread_config=thread_config)
        self.iam = IAM(gcp_facade)

        try:
            self.kubernetesengine = KubernetesEngineConfig(thread_config=thread_config)
        except NameError as _:
            pass

        self.stackdriverlogging = StackdriverLogging(gcp_facade)

    def _is_provider(self, provider_name):
        return provider_name == 'gcp'

    def set_projects(self, projects):
        """
        Set the projects attribute of each of the configs. This is because before authentication (when configs
        are instanciated, the projects within an organization are not known).

        :param projects: List of projects to set
        :return: None
        """

        for c in vars(self):
            setattr(getattr(self, c), 'projects', projects)
