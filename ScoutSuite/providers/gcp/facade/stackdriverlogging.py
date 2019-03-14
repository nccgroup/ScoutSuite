from google.cloud import logging as stackdriver_logging
from ScoutSuite.providers.utils import run_concurrently

class StackdriverLoggingFacade:
    async def get_sinks(self, project_id):
        client = stackdriver_logging.Client(project=project_id)
        return await run_concurrently(lambda: [sink for sink in client.list_sinks()])
