import asyncio
from google.cloud import storage
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently

class CloudStorageFacade:
    async def get_buckets(self, project_id: str):
        client = storage.Client(project=project_id)
        buckets = await run_concurrently(lambda: list(client.list_buckets()))
        await get_and_set_concurrently([self._get_and_set_bucket_logging, 
            self._get_and_set_bucket_iam_policy], buckets)
        return buckets

    async def _get_and_set_bucket_logging(self, bucket):
        bucket_logging = await run_concurrently(lambda: bucket.get_logging())
        setattr(bucket, 'logging', bucket_logging)

    async def _get_and_set_bucket_iam_policy(self, bucket):
        bucket_iam_policy = await run_concurrently(lambda: bucket.get_iam_policy())
        setattr(bucket, 'iam_policy', bucket_iam_policy)
