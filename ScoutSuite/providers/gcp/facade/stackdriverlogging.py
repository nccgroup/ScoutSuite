from google.cloud import logging as stackdriverlogging

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently


class StackdriverLoggingFacade:
    async def get_sinks(self, project_id: str):
        try:
            client = stackdriverlogging.Client(project=project_id)
            return await run_concurrently(lambda: [sink for sink in client.list_sinks()])
        except Exception as e:
            print_exception('Failed to retrieve sinks: {}'.format(e))
            return []
