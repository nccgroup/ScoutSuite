from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class LogProfiles(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for log_profile in await self.facade.loggingmonitoring.get_log_profiles(self.subscription_id):
            id, log_profiles = self._parse_log_profile(log_profile)
            self[id] = log_profiles

    def _parse_log_profile(self, log_profile):
        log_profile_dict = {}

        log_profile_dict['id'] = get_non_provider_id(log_profile.id.lower())
        log_profile_dict['name'] = log_profile.name
        log_profile_dict['storage_account_id'] = log_profile.storage_account_id
        log_profile_dict['service_bus_rule_id'] = log_profile.service_bus_rule_id
        log_profile_dict['retention_policy_enabled'] = log_profile.retention_policy.enabled
        log_profile_dict['retention_policy_days'] = log_profile.retention_policy.days
        log_profile_dict['captures_all_activities'] = self.profile_captures_all_activities(log_profile)

        return log_profile_dict['id'], log_profile_dict

    def profile_captures_all_activities(self, log_profile):
        categories = log_profile.categories
        if 'Delete' in categories and 'Write' in categories and 'Action' in categories:
            return True
        return False

