from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class TransparentDataEncryptions(AzureResources):

    def __init__(self, facade: AzureFacade, resource_group_name: str, server_name: str, database_name: str,
                 subscription_id: str):
        super(TransparentDataEncryptions, self).__init__(facade)
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name
        self.subscription_id = subscription_id

    async def fetch_all(self):
        encryptions = await self.facade.sqldatabase.get_database_transparent_data_encryptions(
            self.resource_group_name, self.server_name, self.database_name, self.subscription_id)
        self._parse_encryptions(encryptions)

    def _parse_encryptions(self, encryptions):
        self.update({
            'transparent_data_encryption_enabled': encryptions.status == "Enabled"
        })
