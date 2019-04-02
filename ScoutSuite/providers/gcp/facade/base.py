from googleapiclient import discovery
from ScoutSuite.providers.gcp.utils import MemoryCache
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils

class GCPBaseFacade:
    def __init__(self, client_name: str, client_version: str):
        self._client_name = client_name
        self._client_version = client_version
        self._client = None

    def _build_client(self) -> discovery.Resource:
        return discovery.build(self._client_name, self._client_version, 
            cache_discovery=False, cache=MemoryCache())

    # Since the HTTP library used by the Google API Client library is not 
    # thread-safe, we need to create a new client for each request.
    def _get_client(self) -> discovery.Resource:
        return self._build_client()