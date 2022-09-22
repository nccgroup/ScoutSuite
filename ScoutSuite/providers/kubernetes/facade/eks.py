from ScoutSuite.providers.kubernetes.authentication_strategy import KubernetesCredentials
from ScoutSuite.providers.kubernetes.facade.base import KubernetesBaseFacade


class EKSFacade(KubernetesBaseFacade):
    cluster = None

    def __init__(self, credentials: KubernetesCredentials, **kwargs):
        super().__init__(credentials)
        self.context = credentials.cluster_context
        self.session = credentials.aws.session
        self.region = self.session.region_name
        self.eks_client = self.session.client('eks', self.region, **kwargs)

    @KubernetesBaseFacade.continue_upon_exception
    def get_cluster(self, **kwargs):
        if not self.cluster:
            self.cluster = self.eks_client.describe_cluster(name=self.context.split('.')[0], **kwargs)
        return self.cluster['cluster']