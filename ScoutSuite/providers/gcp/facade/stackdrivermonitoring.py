from google.cloud import monitoring as stackdrivermonitoring

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently


class StackdriverMonitoringFacade:

    async def get_uptime_checks(self, project_id: str):
        try:
            client = stackdrivermonitoring.UptimeCheckServiceClient()
            name = client.project_path(project_id)
            return await run_concurrently(lambda: [r for r in client.list_uptime_check_configs(name)])
        except Exception as e:
            print_exception('Failed to retrieve uptime checks: {}'.format(e))
            return []

    async def get_alert_policies(self, project_id: str):
        try:
            client = stackdrivermonitoring.AlertPolicyServiceClient()
            name = client.project_path(project_id)
            return await run_concurrently(lambda: [r for r in client.list_alert_policies(name)])
        except Exception as e:
            print_exception('Failed to retrieve alert policies: {}'.format(e))
            return []
