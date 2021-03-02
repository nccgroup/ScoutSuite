from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.core.console import print_exception
from ScoutSuite.utils import get_user_agent
from azure.mgmt.monitor import MonitorManagementClient


class LoggingMonitoringFacade:

    def __init__(self, credentials):
        self.credentials = credentials

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
                lambda: list(client.subscription_diagnostic_settings.list(subscription_id))
            )
            return diagnostic_settings
        except Exception as e:
            print_exception(f'Failed to retrieve diagnostic settings: {e}')
            return []
