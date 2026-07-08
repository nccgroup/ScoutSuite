from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.base.services import BaseServicesConfig
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.kubernetes.authentication_strategy import ClusterProvider, KubernetesCredentials
from ScoutSuite.providers.kubernetes.facade import KubernetesFacade
from ScoutSuite.providers.kubernetes.resources.aks import AKS
from ScoutSuite.providers.kubernetes.resources.base import KubernetesResources
from ScoutSuite.providers.kubernetes.resources.eks import EKS
from ScoutSuite.providers.kubernetes.resources.gke import GKE
from ScoutSuite.providers.kubernetes.resources.workload import Workload
from ScoutSuite.providers.kubernetes.resources.fake_network_policy import FakeNetworkPolicy
from ScoutSuite.providers.kubernetes.resources.rbac import RBAC
from ScoutSuite.providers.kubernetes.resources.version import KubernetesVersions
from ScoutSuite.providers.kubernetes.utils import format_resource_kind

class KubernetesServicesConfig(BaseServicesConfig):
    """Object that holds the necessary Kubernetes configuration for all services in scope."""

    def __init__(self, credentials: KubernetesCredentials):
        super().__init__(credentials)

        if credentials.fetch_local: return

        facade = KubernetesFacade(credentials)

        facade.version.get_versions() # this is here to make sure the cluster is up and running
        self.version = KubernetesVersions(facade)

        core_resources = facade.core.get_resources()
        for name in core_resources:
            _resource = core_resources[name]
            setattr(self, format_resource_kind(name), KubernetesResources(_resource))

        extra_resources = facade.extra.get_resources()
        for name in extra_resources:
            _resource = extra_resources[name]
            setattr(self, format_resource_kind(name), KubernetesResources(_resource))

        self.rbac = RBAC(facade)
        self.workload = Workload(facade)

        if not hasattr(self, 'network_policy'):
            self.network_policy = FakeNetworkPolicy(facade)

        if credentials.cluster_provider == ClusterProvider.AKS.value:
            self.loggingmonitoring = AKS(AzureFacade(credentials.azure))
        elif credentials.cluster_provider == ClusterProvider.EKS.value:
            self.eks = EKS(facade)
        elif credentials.cluster_provider == ClusterProvider.GKE.value:
            self.kubernetesengine = GKE(GCPFacade(credentials.gcp.default_project_id))

    def _is_provider(self, provider_name):
        return provider_name == 'kubernetes'