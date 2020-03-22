from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class Snapshots(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super(Snapshots, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_snapshot in await self.facade.virtualmachines.get_snapshots(self.subscription_id):
            id, snapshot = self._parse_snapshot(raw_snapshot)
            self[id] = snapshot

    def _parse_snapshot(self, raw_snapshot):
        snapshot_dict = {}

        snapshot_dict['id'] = get_non_provider_id(raw_snapshot.id)
        snapshot_dict['name'] = raw_snapshot.name
        snapshot_dict['type'] = raw_snapshot.type
        snapshot_dict['location'] = raw_snapshot.location
        snapshot_dict['tags'] = raw_snapshot.tags
        snapshot_dict['managed_by'] = raw_snapshot.managed_by
        snapshot_dict['sku'] = raw_snapshot.sku
        snapshot_dict['time_created'] = raw_snapshot.time_created
        snapshot_dict['os_type'] = raw_snapshot.os_type
        snapshot_dict['hyper_vgeneration'] = raw_snapshot.hyper_vgeneration
        snapshot_dict['creation_data'] = raw_snapshot.creation_data
        snapshot_dict['disk_size_gb'] = raw_snapshot.disk_size_gb
        snapshot_dict['disk_size_bytes'] = raw_snapshot.disk_size_bytes
        snapshot_dict['unique_id'] = raw_snapshot.unique_id
        snapshot_dict['provisioning_state'] = raw_snapshot.provisioning_state
        snapshot_dict['incremental'] = raw_snapshot.incremental
        snapshot_dict['additional_properties'] = raw_snapshot.additional_properties

        snapshot_dict['encryption'] = raw_snapshot.encryption
        snapshot_dict['encryption_settings_collection'] = raw_snapshot.encryption_settings_collection
        if raw_snapshot.encryption_settings_collection and raw_snapshot.encryption_settings_collection.enabled:
            snapshot_dict['encryption_enabled'] = True
        else:
            snapshot_dict['encryption_enabled'] = False

        return snapshot_dict['id'], snapshot_dict

