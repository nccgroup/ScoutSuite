from ScoutSuite.providers.azure.resources.base import AzureResources


class AutoProvisioningSettings(AzureResources):
    async def fetch_all(self):
        for raw_settings in await self.facade.securitycenter.get_auto_provisioning_settings():
            id, auto_provisioning_settings = self._parse_auto_provisioning_settings(
                raw_settings)
            self[id] = auto_provisioning_settings

    def _parse_auto_provisioning_settings(self, auto_provisioning_settings):
        auto_provisioning_setting_dict = {}
        auto_provisioning_setting_dict['id'] = auto_provisioning_settings.id
        auto_provisioning_setting_dict['name'] = auto_provisioning_settings.name
        auto_provisioning_setting_dict['auto_provision'] = auto_provisioning_settings.auto_provision

        return auto_provisioning_setting_dict['id'], auto_provisioning_setting_dict
