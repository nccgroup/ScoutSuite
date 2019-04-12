import asyncio
from google.cloud import storage
from ScoutSuite.providers.utils import run_concurrently

class CloudStorageFacade:
    async def get_buckets(self, project_id: str):
        client = storage.Client(project=project_id)
        buckets = await run_concurrently(lambda: list(client.list_buckets()))
        if len(buckets) > 0:
            await asyncio.wait({asyncio.ensure_future(self._fetch_additional_bucket_info(bucket)) for bucket in buckets})
        return buckets

    async def _fetch_additional_bucket_info(self, bucket):
        # We're adding new properties to the existing Bucket instance because creating
        # a new dictionary and copying the bucket's __dict__ caused problem since 
        # there are properties that do not have a corresponding attribute. 
        bucket.__dict__['logging'] = await run_concurrently(lambda: bucket.get_logging())
        bucket.__dict__['iam_policy'] = await run_concurrently(lambda: bucket.get_iam_policy())
