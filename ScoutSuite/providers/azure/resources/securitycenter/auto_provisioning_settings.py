from ScoutSuite.providers.base.configs.resources import Resources


class AutoProvisioningSettings(Resources):

    def __init__(self, facade):
        self.facade = facade

    async def fetch_all(self):
        for raw_settings in await self.facade.get_auto_provisioning_settings():
            id, auto_provisioning_settings = self._parse(raw_settings)
            self[id] = auto_provisioning_settings

    def _parse(self, auto_provisioning_setting):
        auto_provisioning_setting_dict = {}
        auto_provisioning_setting_dict['id'] = auto_provisioning_setting.id
        auto_provisioning_setting_dict['name'] = auto_provisioning_setting.name
        auto_provisioning_setting_dict['auto_provision'] = auto_provisioning_setting.auto_provision

        return auto_provisioning_setting_dict['id'], auto_provisioning_setting_dict
