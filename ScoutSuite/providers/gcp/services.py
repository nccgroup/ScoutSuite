from ScoutSuite.providers.base.services import BaseServicesConfig
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.gcp.resources.cloudsql.base import CloudSQL
from ScoutSuite.providers.gcp.resources.cloudstorage.base import CloudStorage
from ScoutSuite.providers.gcp.resources.gce.base import ComputeEngine
from ScoutSuite.providers.gcp.resources.iam.base import IAM
from ScoutSuite.providers.gcp.resources.kms.base import KMS
from ScoutSuite.providers.gcp.resources.stackdriverlogging.base import StackdriverLogging
from ScoutSuite.providers.gcp.resources.stackdrivermonitoring.base import StackdriverMonitoring
from ScoutSuite.providers.gcp.resources.gke.base import KubernetesEngine


class GCPServicesConfig(BaseServicesConfig):

    def __init__(self, credentials=None, default_project_id=None,
                 project_id=None, folder_id=None, organization_id=None, all_projects=None,
                 **kwargs):

        super().__init__(credentials)

        facade = GCPFacade(default_project_id, project_id, folder_id, organization_id, all_projects)

        self.cloudsql = CloudSQL(facade)
        self.cloudstorage = CloudStorage(facade)
        self.computeengine = ComputeEngine(facade)
        self.iam = IAM(facade)
        self.kms = KMS(facade)
        self.stackdriverlogging = StackdriverLogging(facade)
        self.stackdrivermonitoring = StackdriverMonitoring(facade)
        self.kubernetesengine = KubernetesEngine(facade)

    def _is_provider(self, provider_name):
        return provider_name == 'gcp'
