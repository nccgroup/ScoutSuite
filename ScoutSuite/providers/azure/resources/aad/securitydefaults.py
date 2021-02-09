from ScoutSuite.providers.azure.resources.base import AzureResources


class SecurityDefaults(AzureResources):
    async def fetch_all(self):
        raw_security_default = await self.facade.aad.get_security_defaults()
        id, security_default = await self._parse_security_default(raw_security_default)
        self[id] = security_default

    async def _parse_security_default(self, raw_security_default):

        security_default_dict = {}

        security_default_dict['id'] = raw_security_default.get('id')
        security_default_dict['name'] = raw_security_default.get('displayName')
        security_default_dict['is_enabled'] = raw_security_default.get('isEnabled')

        return security_default_dict['id'], security_default_dict
