from oci.object_storage import ObjectStorageClient
from ScoutSuite.providers.oci.authentication_strategy import OracleCredentials
from oci.pagination import list_call_get_all_results

from ScoutSuite.providers.utils import run_concurrently


class ObjectStorageFacade:
    def __init__(self, credentials: OracleCredentials):
        self._credentials = credentials
        self._client = ObjectStorageClient(self._credentials.config)

    async def get_namespace(self):
        response = await run_concurrently(
            lambda: list_call_get_all_results(self._client.get_namespace))
        # for some reason it returns a list of chars instead of a string
        return ''.join(response.data)

    async def get_bucket_details(self, namespace, bucket_name):
        response = await run_concurrently(
            lambda: self._client.get_bucket(namespace, bucket_name))
        return response.data

    async def get_buckets(self, namespace):
        response = await run_concurrently(
            lambda: list_call_get_all_results(self._client.list_buckets, namespace, self._credentials.compartment_id))
        return response.data

    async def get_bucket_objects(self, namespace, bucket_name):
        response = await run_concurrently(
            lambda: list_call_get_all_results(self._client.list_objects, namespace, bucket_name))
        return response.data
