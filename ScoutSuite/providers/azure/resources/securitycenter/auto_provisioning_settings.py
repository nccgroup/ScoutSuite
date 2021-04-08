from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class AutoProvisioningSettings(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_settings in await self.facade.securitycenter.get_auto_provisioning_settings(self.subscription_id):
            id, auto_provisioning_settings = self._parse_auto_provisioning_settings(
                raw_settings)
            self[id] = auto_provisioning_settings

    def _parse_auto_provisioning_settings(self, auto_provisioning_settings):
        auto_provisioning_setting_dict = {}
        auto_provisioning_setting_dict['id'] = get_non_provider_id(auto_provisioning_settings.id)
        auto_provisioning_setting_dict['name'] = auto_provisioning_settings.name
        auto_provisioning_setting_dict['auto_provision'] = auto_provisioning_settings.auto_provision

        return auto_provisioning_setting_dict['id'], auto_provisioning_setting_dict
