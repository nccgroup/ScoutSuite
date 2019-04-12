from ScoutSuite.providers.azure.resources.base import AzureResources


class TransparentDataEncryptions(AzureResources):
    async def fetch_all(self):
        encryptions = await self.facade.sqldatabase.get_database_transparent_data_encryptions(
            self.scope['resource_group_name'], self.scope['server_name'], self.scope['database_name'])
        self._parse_encryptions(encryptions)

    def _parse_encryptions(self, encryptions):
        self.update({
            'transparent_data_encryption_enabled': encryptions.status == "Enabled"
        })
