import datetime

from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently
from ScoutSuite.core.console import print_exception


class StorageAccountsFacade:
    def __init__(self, credentials, subscription_id):
        self._credentials = credentials
        self._subscription_id = subscription_id
        self._client = StorageManagementClient(credentials, subscription_id)

    async def get_storage_accounts(self):
        try:
            storage_accounts = await run_concurrently(
                lambda: list(self._client.storage_accounts.list())
            )
        except Exception as e:
            print_exception('Failed to retrieve storage accounts: {}'.format(e))
            return []
        else:
            await get_and_set_concurrently([self._get_and_set_activity_logs], storage_accounts)
            return storage_accounts

    async def get_blob_containers(self, resource_group_name, storage_account_name):
        try:
            return await run_concurrently(
                lambda: list(self._client.blob_containers.list(resource_group_name, storage_account_name).value)
            )
        except Exception as e:
            print_exception('Failed to retrieve blob containers: {}'.format(e))
            return []

    async def _get_and_set_activity_logs(self, storage_account):
        client = MonitorManagementClient(self._credentials, self._subscription_id)

        # Time format used by Azure API:
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        # Azure API uses UTC time, we need to use the same to avoid bad requests:
        utc_now = datetime.datetime.utcnow()
        # Activity logs are only archived for a period of 90 days max (requesting a timespan of more than that ends up
        # with a bad request):
        timespan = datetime.timedelta(90)

        logs_filter = " and ".join([
            "eventTimestamp ge {}".format((utc_now - timespan).strftime(time_format)),
            "eventTimestamp le {}".format(utc_now.strftime(time_format)),
            "resourceId eq {}".format(storage_account.id),
        ])
        try:
            activity_logs = await run_concurrently(
                lambda: list(client.activity_logs.list(filter=logs_filter, select="eventTimestamp, operationName"))
            )
        except Exception as e:
            print_exception('Failed to retrieve activity logs: {}'.format(e))
            setattr(storage_account, 'activity_logs', [])
        else:
            setattr(storage_account, 'activity_logs', activity_logs)
