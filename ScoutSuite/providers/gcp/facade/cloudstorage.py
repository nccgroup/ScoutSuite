from google.cloud import storage
from google.api_core.gapic_v1.client_info import ClientInfo

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently
from ScoutSuite.utils import get_user_agent


class CloudStorageFacade:

    def get_client(self, project_id: str):
        client_info = ClientInfo(user_agent=get_user_agent())
        client = storage.Client(project=project_id,
                                client_info=client_info)
        return client

    async def get_buckets(self, project_id: str):
        try:
            client = self.get_client(project_id)
            buckets = await run_concurrently(lambda: list(client.list_buckets()))
            await get_and_set_concurrently([self._get_and_set_bucket_logging, 
                self._get_and_set_bucket_iam_policy], buckets)
            return buckets
        except Exception as e:
            print_exception(f'Failed to retrieve storage buckets: {e}')
            return []

    async def _get_and_set_bucket_logging(self, bucket):
        try:
            bucket_logging = await run_concurrently(lambda: bucket.get_logging())
            setattr(bucket, 'logging', bucket_logging)
        except Exception as e:
            print_exception(f'Failed to retrieve bucket logging: {e}')
            setattr(bucket, 'logging', None)

    async def _get_and_set_bucket_iam_policy(self, bucket):
        try:
            bucket_iam_policy = await run_concurrently(lambda: bucket.get_iam_policy())
            setattr(bucket, 'iam_policy', bucket_iam_policy)
        except Exception as e:
            print_exception(f'Failed to retrieve bucket IAM policy: {e}')
            setattr(bucket, 'iam_policy',  None)
