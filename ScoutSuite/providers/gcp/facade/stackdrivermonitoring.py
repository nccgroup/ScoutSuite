from google.cloud import monitoring as stackdrivermonitoring

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently


class StackdriverMonitoringFacade:
    async def get_sinks(self, project_id: str):
        try:
            client = stackdrivermonitoring.MetricServiceClient(project=project_id)
            return await run_concurrently(lambda: [sink for sink in client.list_sinks()])
        except Exception as e:
            print_exception('Failed to retrieve sinks: {}'.format(e))
            return []
