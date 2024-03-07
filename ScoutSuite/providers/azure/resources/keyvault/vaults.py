from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.providers.azure.utils import get_resource_group_name


class Vaults(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_vault in await self.facade.keyvault.get_key_vaults(self.subscription_id):
            id, vault = self._parse_key_vault(raw_vault)
            self[id] = vault

    def _parse_key_vault(self, raw_vault):
        vault = {}
        vault['id'] = get_non_provider_id(raw_vault.id)
        vault['name'] = raw_vault.name
        vault['type'] = raw_vault.type
        vault['location'] = raw_vault.location

        vault['additional_properties'] = raw_vault.additional_properties
        if raw_vault.tags is not None:
            vault['tags'] = ["{}:{}".format(key, value) for key, value in raw_vault.tags.items()]
        else:
            vault['tags'] = []
        vault['resource_group_name'] = get_resource_group_name(raw_vault.id)
        vault['properties'] = raw_vault.properties
        vault[
            'recovery_protection_enabled'] = bool(raw_vault.properties.enable_soft_delete) and \
                                             bool(raw_vault.properties.enable_purge_protection)
        vault['public_access_allowed'] = self._is_public_access_allowed(raw_vault)
        vault['rbac_authorization_enabled'] = raw_vault.properties.enable_rbac_authorization
        vault['private_endpoint_connections'] = self._get_private_endpoint_connections(raw_vault)
        return vault['id'], vault

    def _is_public_access_allowed(self, raw_vault):
        return raw_vault.properties.network_acls is None or raw_vault.properties.network_acls.default_action == 'Allow'
    
    def _get_private_endpoint_connections(self, raw_vault):
        private_endpoint_connections = getattr(raw_vault.properties, "private_endpoint_connections", None)
        if not private_endpoint_connections:
            return []
        return [pe.private_endpoint.id for pe in private_endpoint_connections if pe.private_link_service_connection_state.status == 'Approved']
