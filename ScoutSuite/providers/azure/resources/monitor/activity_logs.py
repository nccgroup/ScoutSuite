from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.azure.facade.monitor import MonitorFacade
from ScoutSuite.providers.utils import get_non_provider_id


class ActivityLogs(Resources):

    async def fetch_all(self, credentials, **kwargs):
        # TODO: build that facade somewhere else:
        facade = MonitorFacade(credentials.credentials, credentials.subscription_id)

        self['activity_logs'] = {}
        self['activity_logs']['storage_accounts'] = {}

        for raw_log in await facade.get_activity_logs():
            self._parse(raw_log)

    def _parse(self, raw_log):
        if raw_log.resource_type.value == 'Microsoft.Storage/storageAccounts':
            self._parse_storage_account_log(raw_log)

    def _parse_storage_account_log(self, raw_log):
            storage_account_id = get_non_provider_id(raw_log.resource_id.lower())

            if storage_account_id not in self['activity_logs']['storage_accounts']:
                self['activity_logs']['storage_accounts'][storage_account_id] =\
                    {'access_keys_rotated': False}

            if raw_log.operation_name.value == 'Microsoft.Storage/storageAccounts/regenerateKey/action':
                self['activity_logs']['storage_accounts'][storage_account_id]['access_keys_rotated'] = True
