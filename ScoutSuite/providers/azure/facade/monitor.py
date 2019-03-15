import datetime

from azure.mgmt.monitor import MonitorManagementClient
from ScoutSuite.providers.utils import run_concurrently


class MonitorFacade:
    def __init__(self, credentials, subscription_id):
        self._client = MonitorManagementClient(credentials, subscription_id)

    async def get_activity_logs(self):
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        utc_now = datetime.datetime.utcnow()
        end_time = utc_now.strftime(time_format)
        timespan = datetime.timedelta(90)  # 90 days of timespan
        start_time = (utc_now - timespan).strftime(time_format)

        return await run_concurrently(
            lambda: self._client.activity_logs.list(
                filter="eventTimestamp ge {} and eventTimestamp le {}".format(start_time, end_time))
        )
