from google.cloud import storage

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently


class CloudStorageFacade:
    async def get_buckets(self, project_id: str):
        try:
            client = storage.Client(project=project_id)
            buckets = await run_concurrently(lambda: list(client.list_buckets()))
            await get_and_set_concurrently([self._get_and_set_bucket_logging, 
                self._get_and_set_bucket_iam_policy], buckets)
            return buckets
        except Exception as e:
            print_exception('Failed to retrieve storage buckets: {}'.format(e))
            return []

    async def _get_and_set_bucket_logging(self, bucket):
        try:
            bucket_logging = await run_concurrently(lambda: bucket.get_logging())
            setattr(bucket, 'logging', bucket_logging)
        except Exception as e:
            print_exception('Failed to retrieve bucket logging: {}'.format(e))
            setattr(bucket, 'logging', None)

    async def _get_and_set_bucket_iam_policy(self, bucket):
        try:
            bucket_iam_policy = await run_concurrently(lambda: bucket.get_iam_policy())
            setattr(bucket, 'iam_policy', bucket_iam_policy)
        except Exception as e:
            print_exception('Failed to retrieve bucket IAM policy: {}'.format(e))
            setattr(bucket, 'iam_policy',  None)
