from ScoutSuite.providers.base.configs.resources import Resources


class TransparentDataEncryptions(Resources):

    def __init__(self, resource_group_name, server_name, database_name, facade):
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name
        self.facade = facade

    async def fetch_all(self):
        encryptions = await self.facade.get_database_transparent_data_encryptions(
            self.resource_group_name, self.server_name, self.database_name)
        self._parse_encryptions(encryptions)

    def _parse_encryptions(self, encryptions):
        self.update({
            'transparent_data_encryption_enabled': encryptions.status == "Enabled"
        })
