from google.cloud import logging as stackdriverlogging
from google.api_core.gapic_v1.client_info import ClientInfo

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.utils import get_user_agent


class StackdriverLoggingFacade:

    def get_client(self, project_id: str):
        client_info = ClientInfo(user_agent=get_user_agent())
        client = stackdriverlogging.Client(project=project_id,
                                           client_info=client_info)
        return client

    async def get_sinks(self, project_id: str):
        try:
            client = self.get_client(project_id)
            return await run_concurrently(lambda: [sink for sink in client.list_sinks()])
        except Exception as e:
            print_exception(f'Failed to retrieve sinks: {e}')
            return []

    async def get_metrics(self, project_id: str):
        try:
            client = self.get_client(project_id)
            return await run_concurrently(lambda: [metric for metric in client.list_metrics()])
        except Exception as e:
            print_exception(f'Failed to retrieve metrics: {e}')
            return []
