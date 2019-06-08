from ScoutSuite.providers.aliyun.resources.base import AliyunResources


class Actiontrail(AliyunResources):
    async def fetch_all(self):
        # TODO parse trails
        # should create a trail and see what is returned
        raw_trails = await  self.facade.actiontrail.describe_trails()
        return self._parse_actiontrails(raw_trails)
        # self['trails'] = {}
        # for raw_vault in await self.facade.keyvault.get_key_vaults():
        #     id, vault = self._parse_key_vault(raw_vault)
        #     self['vaults'][id] = vault
        #
        # self['vaults_count'] = len(self['vaults'])

    def _parse_actiontrails(self, raw_actiontrail):
        return {}

        # vault = {}
        # vault['id'] = get_non_provider_id(raw_vault.id)
        # vault['name'] = raw_vault.name
        # vault['public_access_allowed'] = self._is_public_access_allowed(raw_vault)
        #
        # return vault['id'], vault
