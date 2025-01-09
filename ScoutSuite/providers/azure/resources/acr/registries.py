from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class Registries(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_registry in await self.facade.acr.get_registries(self.subscription_id):
            id, registry = self._parse_registry(raw_registry)
            self[id] = registry

    def _parse_registry(self, raw_registry):

        registry = {}
        registry['id'] = get_non_provider_id(raw_registry.id)
        registry['name'] = raw_registry.name
        registry['type'] = raw_registry.type
        registry['location'] = raw_registry.location
        if raw_registry.tags is not None:
            registry['tags'] = ["{}:{}".format(key, value) for key, value in  raw_registry.tags.items()]
        else:
            registry['tags'] = []

        registry['sku'] = {}
        registry['sku']['name'] = raw_registry.sku.name
        registry['sku']['tier'] = raw_registry.sku.tier
        
        registry['identity'] = raw_registry.identity
        registry['login_server'] = raw_registry.login_server
        registry['provisioning_state'] = raw_registry.provisioning_state
        registry['status'] = raw_registry.status
        registry['admin_user_enabled'] = bool(raw_registry.admin_user_enabled)
        registry['network_rule_set'] = raw_registry.network_rule_set

        registry['policies'] = {
            'azureAD_authentication_policy': {},
            'soft_delete_policy': {},
            'quarantine_policy': {},
            'trust_policy': {},
            'retention_policy': {},
            'export_policy': {}
        }
        
        registry['policies']['azureAD_suthentication_policy'] = raw_registry.policies.additional_properties['azureADAuthenticationAsArmPolicy']

        registry['policies']['soft_delete_policy']['retention_days'] = raw_registry.policies.additional_properties['softDeletePolicy']['retentionDays']
        registry['policies']['soft_delete_policy']['status'] = raw_registry.policies.additional_properties['softDeletePolicy']['status']
        
        registry['policies']['quarantine_policy']['status'] = raw_registry.policies.quarantine_policy.status

        registry['policies']['trust_policy']['status'] = raw_registry.policies.trust_policy.status
        registry['policies']['trust_policy']['type'] = raw_registry.policies.trust_policy.type

        registry['policies']['retention_policy']['status'] = raw_registry.policies.retention_policy.status
        registry['policies']['retention_policy']['type'] = raw_registry.policies.retention_policy.days

        registry['policies']['export_policy']['status'] = raw_registry.policies.export_policy.status

        registry['encryption'] = {}
        registry['encryption']['status'] = raw_registry.encryption.status
        registry['encryption']['key_vault_properties'] = raw_registry.encryption.key_vault_properties

        registry['data_endpoint_enabled'] = bool(raw_registry.data_endpoint_enabled) 
        registry['data_endpoint_host_names'] = raw_registry.data_endpoint_host_names
        registry['private_endpoint_connections'] = raw_registry.private_endpoint_connections
        registry['public_network_access'] = raw_registry.public_network_access
        registry['network_rule_bypass_options'] = raw_registry.network_rule_bypass_options
        registry['zone_redundancy'] = raw_registry.zone_redundancy
        
        return registry['id'], registry