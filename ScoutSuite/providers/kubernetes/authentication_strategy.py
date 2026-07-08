import logging
import enum

from google.auth.credentials import Credentials as GCPCredentials
from kubernetes import config, client
from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy
from ScoutSuite.providers.aws.authentication_strategy import AWSAuthenticationStrategy, AWSCredentials
from ScoutSuite.providers.azure.authentication_strategy import AzureAuthenticationStrategy, AzureCredentials
from ScoutSuite.providers.gcp.authentication_strategy import GCPAuthenticationStrategy


class KubernetesCredentials:
    def __init__(self) -> None:
        self.cluster_provider: str = None
        self.cluster_context: str = None
        self.api_client: client.ApiClient = None
        self.fetch_local: bool = False
        
        self.aws: AWSCredentials = None
        self.azure: AzureCredentials = None
        self.gcp: GCPCredentials = None

class ClusterProvider(enum.Enum):
    # Azure
    AKS = 'aks'
    # AWS
    EKS = 'eks'
    # GCP
    GKE = 'gke'

class ResourceTemplates(enum.Enum):
    RESOURCE_CONTAINERS = 'kubernetes_resource_containers'
    RESOURCE_HOST = 'kubernetes_resource_host'

class KubernetesAuthenticationStrategy(AuthenticationStrategy):
    '''
    Implements authentication for the Kubernetes provider.
    '''

    def authenticate(self, **kwargs):
        '''Obtain credentials to interact with the Kubernetes cluster'''

        logging.getLogger('kubernetes.client.rest').setLevel(logging.ERROR)

        cluster_provider = kwargs.get('kubernetes_cluster_provider')
        config_file = kwargs.get('kubernetes_config_file')
        context = kwargs.get('kubernetes_context')
        persist_config = kwargs.get('kubernetes_persist_config')
        fetch_local = kwargs.get('kubernetes_fetch_local')

        credentials = KubernetesCredentials()
        if cluster_provider in [ClusterProvider.AKS.value]:
            subscription_id = subscription_id=kwargs.get('kubernetes_azure_subscription_id')
            credentials.azure = AzureAuthenticationStrategy().authenticate(cli=True, subscription_id=subscription_id)

        elif cluster_provider in [ClusterProvider.EKS.value]:
            credentials.aws = AWSAuthenticationStrategy().authenticate()

        elif cluster_provider in [ClusterProvider.GKE.value]:
            credentials.gcp = GCPAuthenticationStrategy().authenticate(user_account=True)

        config.load_kube_config(config_file, context, None, persist_config)

        credentials.cluster_provider = cluster_provider
        credentials.cluster_context = context or config.list_kube_config_contexts(config_file)[1]['context']['cluster']
        credentials.api_client = config.new_client_from_config(config_file, context, persist_config)
        credentials.fetch_local = fetch_local

        return credentials
