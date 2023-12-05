from ScoutSuite.core.console import print_info
from ScoutSuite.providers.kubernetes.facade.base import KubernetesBaseFacade


class VersionFacade(KubernetesBaseFacade):
    def __init__(self, credentials):
        super().__init__(credentials)

    def get_versions(self) -> dict:
        if self.data != None:
            return self.data

        self.data = self.get('/version')

        return self.data
