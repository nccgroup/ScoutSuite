from ScoutSuite.providers.kubernetes.resources.base import KubernetesResourcesWithFacade


class KubernetesVersions(KubernetesResourcesWithFacade):
    async def fetch_all(self):
        details = self.facade.version.get_versions()
        self['details'] = {
            'v1': details
        }
        self['details_count'] = len(details)
