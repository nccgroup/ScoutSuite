from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class ServerEncryptionProtectors(AzureResources):

    def __init__(self, facade: AzureFacade, resource_group_name: str, server_name: str, subscription_id: str):
        super().__init__(facade)
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.subscription_id = subscription_id

    async def fetch_all(self):
        protectors = await self.facade.sqldatabase.get_server_encryption_protectors(
            self.resource_group_name, self.server_name, self.subscription_id)
        self._parse_protectors(protectors)

    def _parse_protectors(self, protectors):
        self.update({
            'kind': protectors.kind,
            'server_key_type': protectors.server_key_type,
            'uri': protectors.uri,
            'TDE_protector_is_encrypted': protectors.kind == 'azurekeyvault' and
            protectors.server_key_type == 'AzureKeyVault' and protectors.uri is not None
        })
