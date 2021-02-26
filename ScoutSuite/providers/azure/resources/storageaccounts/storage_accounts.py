from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureCompositeResources
from ScoutSuite.providers.azure.utils import get_resource_group_name
from ScoutSuite.providers.utils import get_non_provider_id

from .blob_containers import BlobContainers
# from .queues import Queues
from .blob_services import BlobServices


class StorageAccounts(AzureCompositeResources):
    _children = [
        (BlobContainers, 'blob_containers'),
        (BlobServices, 'blob_services'),
        # (Queues, 'queues')  # FIXME - not implemented by SDK
    ]

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_storage_account in await self.facade.storageaccounts.get_storage_accounts(self.subscription_id):
            id, storage_account = self._parse_storage_account(raw_storage_account)
            self[id] = storage_account

        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={storage_account_id: {'resource_group_name': storage_account['resource_group_name'],
                                         'storage_account_name': storage_account['name'],
                                         'subscription_id': self.subscription_id}
                    for (storage_account_id, storage_account) in self.items()}
        )

    def _parse_storage_account(self, raw_storage_account):
        storage_account = {}

        encryption = raw_storage_account.encryption
        raw_id = raw_storage_account.id
        storage_account['id'] = get_non_provider_id(raw_id.lower())
        storage_account['resource_group_name'] = get_resource_group_name(raw_id)
        storage_account['name'] = raw_storage_account.name
        storage_account['https_traffic_enabled'] = raw_storage_account.enable_https_traffic_only
        storage_account['public_traffic_allowed'] = self._is_public_traffic_allowed(raw_storage_account)
        storage_account['trusted_microsoft_services_enabled'] = \
            self._is_trusted_microsoft_services_enabled(raw_storage_account)
        storage_account['bypass'] = raw_storage_account.network_rule_set.bypass
        storage_account['access_keys_last_rotation_date'] = \
            self._parse_access_keys_last_rotation_date(raw_storage_account.activity_logs)
        storage_account['encryption_key_source'] = raw_storage_account.encryption.key_source
        storage_account['encryption_key_customer_managed'] = self._is_encryption_key_customer_managed(raw_storage_account.encryption.key_source)
        if raw_storage_account.tags is not None:
            storage_account['tags'] = ["{}:{}".format(key, value) for key, value in  raw_storage_account.tags.items()]
        else:
            storage_account['tags'] = []

        return storage_account['id'], storage_account

    def _is_public_traffic_allowed(self, storage_account):
        return storage_account.network_rule_set.default_action == "Allow"

    def _is_trusted_microsoft_services_enabled(self, storage_account):
        if storage_account.network_rule_set.bypass:
            return "AzureServices" in storage_account.network_rule_set.bypass
        return False

    def _parse_access_keys_last_rotation_date(self, activity_logs):
        last_rotation_date = None
        for log in activity_logs:
            if log.operation_name.value == 'Microsoft.Storage/storageAccounts/regenerateKey/action':
                if last_rotation_date is None or last_rotation_date < log.event_timestamp:
                    last_rotation_date = log.event_timestamp
        return last_rotation_date

    def _is_encryption_key_customer_managed(self, key_source):
        # Microsoft Storage is the default option which is not customer-managed
        return key_source != "Microsoft.Storage"

