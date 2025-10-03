from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.core.console import print_exception
from ScoutSuite.utils import get_user_agent
from azure.mgmt.monitor import MonitorManagementClient
import asyncio
import requests


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
            try:
                log_profiles = await run_concurrently(
                    lambda: list(client.log_profiles.list())
                )
            except AttributeError as ae:
                if 'throttler' in str(ae):
                    loop = asyncio.get_event_loop()
                    log_profiles = await loop.run_in_executor(
                        None, lambda: list(client.log_profiles.list())
                    )
                else:
                    raise
            return log_profiles
        except Exception as e:
            print_exception(f'Failed to retrieve log profiles: {e}')
            return []

    async def get_subscription_diagnostic_settings(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            if hasattr(client, 'subscription_diagnostic_settings'):
                try:
                    diagnostic_settings = await run_concurrently(
                        lambda: client.subscription_diagnostic_settings.list(subscription_id).value
                    )
                except AttributeError as ae:
                    if 'throttler' in str(ae):
                        loop = asyncio.get_event_loop()
                        diagnostic_settings = await loop.run_in_executor(
                            None, lambda: client.subscription_diagnostic_settings.list(subscription_id).value
                        )
                    else:
                        raise
                return diagnostic_settings
            else:
                # Fallback to REST API when SDK does not expose subscription_diagnostic_settings
                loop = asyncio.get_event_loop()

                def _fetch_subscription_diag_settings():
                    token = self.credentials.get_credentials().get_token("https://management.azure.com/.default").token
                    headers = {'Authorization': f'Bearer {token}'}
                    url = f'https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Insights/diagnosticSettings?api-version=2017-05-01-preview'
                    resp = requests.get(url, headers=headers, timeout=30)
                    if resp.status_code == 200:
                        return resp.json().get('value', [])
                    if resp.status_code == 404:
                        return []
                    raise Exception(f'HTTP {resp.status_code} from {url}')

                return await loop.run_in_executor(None, _fetch_subscription_diag_settings)
        except Exception as e:
            print_exception(f'Failed to retrieve subscription diagnostic settings: {e}')
            return []

    async def get_diagnostic_settings(self, subscription_id: str, resource_id: str):
        try:
            client = self.get_client(subscription_id)
            try:
                diagnostic_settings = await run_concurrently(
                    lambda: client.diagnostic_settings.list(resource_id).value
                )
            except AttributeError as ae:
                if 'throttler' in str(ae):
                    loop = asyncio.get_event_loop()
                    diagnostic_settings = await loop.run_in_executor(
                        None, lambda: client.diagnostic_settings.list(resource_id).value
                    )
                else:
                    raise
            return diagnostic_settings
        except Exception as e:
            print_exception(f'Failed to retrieve resource diagnostic settings: {e}')
            return []

    async def get_activity_log_alerts(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            try:
                activity_log_alerts = await run_concurrently(
                    lambda: list(client.activity_log_alerts.list_by_subscription_id())
                )
            except AttributeError as ae:
                if 'throttler' in str(ae):
                    loop = asyncio.get_event_loop()
                    activity_log_alerts = await loop.run_in_executor(
                        None, lambda: list(client.activity_log_alerts.list_by_subscription_id())
                    )
                else:
                    raise
            return activity_log_alerts
        except Exception as e:
            print_exception(f'Failed to retrieve activity log alerts: {e}')
            return []
