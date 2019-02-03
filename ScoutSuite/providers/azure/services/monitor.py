# -*- coding: utf-8 -*-

import datetime

from ScoutSuite.providers.azure.configs.base import AzureBaseConfig


class MonitorConfig(AzureBaseConfig):
    time_format = "%Y-%m-%dT%H:%M:%S.%f"
    utc_now = datetime.datetime.utcnow()
    end_time = utc_now.strftime(time_format)
    timespan = datetime.timedelta(90)  # 90 days of timespan
    start_time = (utc_now - timespan).strftime(time_format)

    targets = (
        ('activity_logs', 'Activity Logs', 'list',
         {'filter': "eventTimestamp ge {} and eventTimestamp le {}".format(start_time, end_time)},
         False),
    )

    def __init__(self, thread_config):

        self.activity_logs = {}
        self.activity_logs['storage_accounts'] = {}

        super(MonitorConfig, self).__init__(thread_config)

    def parse_activity_logs(self, activity_log, params):
        if activity_log.resource_type.value == 'Microsoft.Storage/storageAccounts':
            self._parse_storage_account_logs(activity_log)

    def _parse_storage_account_logs(self, activity_log):
            storage_account_id = self.get_non_provider_id(activity_log.resource_id.lower())

            if storage_account_id not in self.activity_logs['storage_accounts']:
                self.activity_logs['storage_accounts'][storage_account_id] =\
                    {'access_keys_rotated': False}
                
            if activity_log.operation_name.value == 'Microsoft.Storage/storageAccounts/regenerateKey/action':
                self.activity_logs['storage_accounts'][storage_account_id]['access_keys_rotated'] = True
