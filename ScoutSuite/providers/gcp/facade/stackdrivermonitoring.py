from google.cloud import monitoring as stackdrivermonitoring
from google.api_core.gapic_v1.client_info import ClientInfo

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.utils import get_user_agent


class StackdriverMonitoringFacade:
    # TODO find a way to skip the project if it's not configured as a stackdriver workspace

    def get_uptime_client(self):
        client_info = ClientInfo(user_agent=get_user_agent())
        client = stackdrivermonitoring.UptimeCheckServiceClient(client_info=client_info)
        return client

    def get_alerts_client(self):
        client_info = ClientInfo(user_agent=get_user_agent())
        client = stackdrivermonitoring.AlertPolicyServiceClient(client_info=client_info)
        return client

    async def get_uptime_checks(self, project_id: str):
        try:
            client = self.get_uptime_client()
            name = client.project_path(project_id)
            return await run_concurrently(lambda: [r for r in client.list_uptime_check_configs(name)])
        except Exception as e:
            if 'is not a workspace' not in getattr(e, 'message', '') and '404' not in str(e):
                print_exception(f'Failed to retrieve uptime checks: {e}')
            return []

    async def get_alert_policies(self, project_id: str):
        try:
            client = self.get_alerts_client()
            name = client.project_path(project_id)
            return await run_concurrently(lambda: [r for r in client.list_alert_policies(name)])
        except Exception as e:
            if 'is not a workspace' not in getattr(e, 'message', '') and '404' not in str(e):
                print_exception(f'Failed to retrieve alert policies: {e}')
            return []
