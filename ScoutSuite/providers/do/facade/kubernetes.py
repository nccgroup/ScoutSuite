from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.do.authentication_strategy import DoCredentials
from ScoutSuite.providers.utils import run_concurrently


class KubernetesDoFacade:
    def __init__(self, credentials: DoCredentials):
        self._credentials = credentials
        self._client = credentials.client

    async def get_kubernetes(self):
        try:
            kubernetes = await run_concurrently(
                lambda: self._client.kubernetes.list_clusters()["kubernetes_clusters"]
            )
            return kubernetes
        except Exception as e:
            print_exception(f"Failed to get kubernetes clusters: {e}")
            return []

    