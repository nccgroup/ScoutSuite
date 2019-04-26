from googleapiclient import discovery

class GCPBaseFacade:
    def __init__(self, client_name: str, client_version: str):
        self._client_name = client_name
        self._client_version = client_version
        self._client = None

    def _build_client(self) -> discovery.Resource:
        return self._build_arbitrary_client(self._client_name, self._client_version)

    def _build_arbitrary_client(self, client_name, client_version):
        return discovery.build(client_name, client_version, cache_discovery=False, cache=MemoryCache())

    # Since the HTTP library used by the Google API Client library is not 
    # thread-safe, we need to create a new client for each request.
    def _get_client(self) -> discovery.Resource:
        return self._build_client()


class MemoryCache:
    """
    Workaround https://github.com/googleapis/google-api-python-client/issues/325#issuecomment-274349841
    """
    _cache = {}

    def get(self, url):
        return MemoryCache._cache.get(url)

    def set(self, url, content):
        MemoryCache._cache[url] = content
