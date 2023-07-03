from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.providers.azure.utils import get_resource_group_name

from datetime import datetime, timezone

class Vaults(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_vault in await self.facade.keyvault.get_key_vaults(self.subscription_id):
            id, vault = self._parse_key_vault(raw_vault)
            self[id] = vault
            vault['keys'] = await self.fetch_keys(vault['resource_group_name'], vault['name'])
            vault['secrets'] = await self.fetch_secrets(vault['resource_group_name'], vault['name'])
            
    async def fetch_keys(self, resource_group_name, keyvault_name):
        keys = []
        try:
            for raw_key in await self.facade.keyvault.get_keys(self.subscription_id, resource_group_name, keyvault_name):
                raw_key_extra = await self.facade.keyvault.get_key(self.subscription_id, resource_group_name, keyvault_name, raw_key.name)
                key = self._parse_key(raw_key, raw_key_extra)
                keys.append(key)
        except Exception as e:
            print_exception(f'Failed to list Keys in Key Vault {keyvault_name}: {e}')
            return []
        return keys

    async def fetch_secrets(self, resource_group_name, keyvault_name):
        secrets = []
        try:
            for raw_secret in await self.facade.keyvault.get_secrets(self.subscription_id,resource_group_name, keyvault_name):
                secret = self._parse_secret(raw_secret)
                secrets.append(secret)
        except Exception as e:
            print_exception(f'Failed to list Secrets in Key Vault {keyvault_name}: {e}')
            return []
        return secrets

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
            'recovery_protection_enabled'] = raw_vault.properties.enable_soft_delete and \
                                             bool(raw_vault.properties.enable_purge_protection)
        vault['public_access_allowed'] = self._is_public_access_allowed(raw_vault)
        vault['rbac_authorization_enabled'] = raw_vault.properties.enable_rbac_authorization
        return vault['id'], vault

    def _is_public_access_allowed(self, raw_vault):
        return raw_vault.properties.network_acls is None or raw_vault.properties.network_acls.default_action == 'Allow'
    
    def _parse_key(self, raw_key, raw_key_extra):
        raw_attrs = raw_key.attributes
        key = {}
        key['id'] = get_non_provider_id(raw_key.id)
        key['name'] = raw_key.name
        key['enabled'] = raw_attrs.enabled
        key['expires'] = datetime.fromtimestamp(raw_attrs.expires, tz=timezone.utc) if raw_attrs.expires else None
        key['not_before'] = datetime.fromtimestamp(raw_attrs.not_before, tz=timezone.utc) if raw_attrs.not_before else None
        key['exportable'] = raw_attrs.exportable
        key['recovery_level'] = raw_attrs.recovery_level
        key['auto_rotation_enabled'] = self._is_auto_rotation_enabled(raw_key_extra.rotation_policy)
        return key

    def _parse_secret(self, raw_secret):
        raw_attrs = raw_secret.properties.attributes
        secret = {}
        secret['id'] = get_non_provider_id(raw_secret.id)
        secret['name'] = raw_secret.name
        secret['enabled'] = raw_attrs.enabled
        secret['expires'] = raw_attrs.expires
        secret['not_before'] = raw_attrs.not_before
        return secret
    
    def _is_auto_rotation_enabled(self, rotation_policy):
        if rotation_policy is None or rotation_policy.lifetime_actions is None:
            return False
        return any(la for la in rotation_policy.lifetime_actions if la.action.type == 'rotate')