# -*- coding: utf-8 -*-

import datetime

from ScoutSuite.providers.azure.configs.base import AzureBaseConfig


class MonitorConfig(AzureBaseConfig):

    list_filter = " and ".join([
        "eventTimestamp ge {}".format(datetime.datetime.now() - datetime.timedelta(days=90)),  # after 90 days ago
        "eventTimestamp le {}".format(datetime.datetime.now()),  # before today
        # The below filter makes the query *significantly* faster
        # Additional resources should be included as required
        "resourceProvider eq {}".format('Microsoft.Storage'),
    ])

    targets = (
        ('activity_logs', 'Activity Logs', 'list',
         {'filter': list_filter},
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
                self.activity_logs['storage_accounts'][storage_account_id] = {'access_keys_last_rotation_date': None}

            if activity_log.operation_name.value == 'Microsoft.Storage/storageAccounts/regenerateKey/action':
                if not self.activity_logs['storage_accounts'][storage_account_id]['access_keys_last_rotation_date'] or \
                        activity_log.event_timestamp < \
                        self.activity_logs['storage_accounts'][storage_account_id]['access_keys_last_rotation_date']:
                    self.activity_logs['storage_accounts'][storage_account_id]['access_keys_last_rotation_date'] = \
                        activity_log.event_timestamp
