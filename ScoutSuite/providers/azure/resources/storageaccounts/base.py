from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .storage_accounts import StorageAccounts


class StorageAccounts(Subscriptions):
    _children = [
        (StorageAccounts, 'storage_accounts')
    ]

