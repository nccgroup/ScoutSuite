from ScoutSuite.providers.kubernetes.resources.base import KubernetesResourcesWithFacade


class FakeNetworkPolicy(KubernetesResourcesWithFacade):
    '''Created to display network policy findings in the event that the cluster has no network policies.'''

    async def fetch_all(self):
        self['v1'] = {}
        self['v1_count'] = 0