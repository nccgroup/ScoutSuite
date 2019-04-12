from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.providers.gcp.facade.gcp import GCPFacade
from ScoutSuite.providers.gcp.resources.cloudresourcemanager.base import CloudResourceManager
from ScoutSuite.providers.gcp.resources.cloudsql.base import CloudSQL
from ScoutSuite.providers.gcp.resources.cloudstorage.base import CloudStorage
from ScoutSuite.providers.gcp.resources.gce.base import ComputeEngine
from ScoutSuite.providers.gcp.resources.iam.base import IAM
from ScoutSuite.providers.gcp.resources.stackdriverlogging.base import StackdriverLogging

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
        self.cloudsql = CloudSQL(gcp_facade)
        self.cloudstorage = CloudStorage(gcp_facade)
        self.computeengine = ComputeEngine(gcp_facade)
        self.iam = IAM(gcp_facade)

        try:
            self.kubernetesengine = KubernetesEngineConfig(thread_config=thread_config)
        except NameError as _:
            pass

        self.stackdriverlogging = StackdriverLogging(gcp_facade)

    def _is_provider(self, provider_name):
        return provider_name == 'gcp'
