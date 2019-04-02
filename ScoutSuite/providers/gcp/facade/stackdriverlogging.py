from google.cloud import logging as stackdriverlogging
from ScoutSuite.providers.utils import run_concurrently

class StackdriverLoggingFacade:
    async def get_sinks(self, project_id: str):
        client = stackdriverlogging.Client(project=project_id)
        return await run_concurrently(lambda: [sink for sink in client.list_sinks()])
