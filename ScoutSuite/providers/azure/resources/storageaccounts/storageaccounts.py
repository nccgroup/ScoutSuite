from ScoutSuite.providers.azure.resources.resources import AzureCompositeResources
from ScoutSuite.providers.azure.utils import get_resource_group_name
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.providers.azure.facade.storageaccounts import StorageAccountsFacade

from .blob_containers import BlobContainers


class StorageAccounts(AzureCompositeResources):
    _children = [
        (BlobContainers, 'blob_containers')
    ]

    async def fetch_all(self, credentials, **kwargs):
        # TODO: build that facade somewhere else:
        facade = StorageAccountsFacade(credentials.credentials, credentials.subscription_id)

        self['storage_accounts'] = {}
        for raw_storage_account in await facade.get_storage_accounts():
            id, storage_account = self._parse(raw_storage_account)
            self['storage_accounts'][id] = storage_account
        self['storage_accounts_count'] = len(self['storage_accounts'])

        await self._fetch_children_of_all_resources(
            resources=self['storage_accounts'],
            kwargs={storage_account_id: {'resource_group_name': storage_account['resource_group_name'],
                                         'storage_account_name': storage_account['name'],
                                         'facade': facade}
                    for (storage_account_id, storage_account) in self['storage_accounts'].items()}
        )

    def _parse(self, raw_storage_account):
        storage_account = {}
        raw_id = raw_storage_account.id
        storage_account['id'] = get_non_provider_id(raw_id.lower())
        storage_account['resource_group_name'] = get_resource_group_name(raw_id)
        storage_account['name'] = raw_storage_account.name
        storage_account['https_traffic_enabled'] = raw_storage_account.enable_https_traffic_only
        storage_account['public_traffic_allowed'] = self._is_public_traffic_allowed(raw_storage_account)

        return storage_account['id'], storage_account

    def _is_public_traffic_allowed(self, storage_account):
        return storage_account.network_rule_set.default_action == "Allow"

