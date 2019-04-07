from google.cloud import storage
from ScoutSuite.providers.utils import run_concurrently

class CloudStorageFacade:
    async def get_buckets(self, project_id: str):
        client = storage.Client(project=project_id)
        return await run_concurrently(lambda: list(client.list_buckets()))
