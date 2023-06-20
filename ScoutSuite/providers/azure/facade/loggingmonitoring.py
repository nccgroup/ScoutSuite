from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.core.console import print_exception
from ScoutSuite.utils import get_user_agent
from azure.mgmt.monitor import MonitorManagementClient


class LoggingMonitoringFacade:

    def __init__(self, credentials, resource_group=None):
        self.credentials = credentials
        self.resource_group = resource_group

    def get_client(self, subscription_id: str):
        client = MonitorManagementClient(self.credentials.get_credentials(),
                                         subscription_id=subscription_id,
                                         user_agent=get_user_agent())
        return client

    async def get_log_profiles(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            log_profiles = await run_concurrently(
                lambda: list(client.log_profiles.list())
            )
            return log_profiles
        except Exception as e:
            print_exception(f'Failed to retrieve log profiles: {e}')
            return []

    async def get_subscription_diagnostic_settings(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            diagnostic_settings = await run_concurrently(
                lambda: client.subscription_diagnostic_settings.list(subscription_id).value
            )
            return diagnostic_settings
        except Exception as e:
            print_exception(f'Failed to retrieve subscription diagnostic settings: {e}')
            return []

    async def get_diagnostic_settings(self, subscription_id: str, resource_id: str):
        try:
            client = self.get_client(subscription_id)
            diagnostic_settings = await run_concurrently(
                lambda: client.diagnostic_settings.list(resource_id).value
            )
            return diagnostic_settings
        except Exception as e:
            print_exception(f'Failed to retrieve resource diagnostic settings: {e}')
            return []

    async def get_activity_log_alerts(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            if self.resource_group:
                activity_log_alerts = await run_concurrently(
                    lambda: list(client.activity_log_alerts.list_by_resource_group(resource_group_name=self.resource_group))
                )
            else:
                activity_log_alerts = await run_concurrently(
                    lambda: list(client.activity_log_alerts.list_by_subscription_id())
                )
            return activity_log_alerts
        except Exception as e:
            print_exception(f'Failed to retrieve activity log alerts: {e}')
            return []
