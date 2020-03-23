from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class Disks(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super(Disks, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_disk in await self.facade.virtualmachines.get_disks(self.subscription_id):
            id, disk = self._parse_disk(raw_disk)
            self[id] = disk

    def _parse_disk(self, raw_disk):
        disk_dict = {}
        disk_dict['id'] = get_non_provider_id(raw_disk.id)
        disk_dict['name'] = raw_disk.name
        disk_dict['type'] = raw_disk.type
        disk_dict['location'] = raw_disk.location
        disk_dict['tags'] = raw_disk.tags
        disk_dict['managed_by'] = raw_disk.managed_by
        disk_dict['sku'] = raw_disk.sku
        disk_dict['zones'] = raw_disk.zones
        disk_dict['time_created'] = raw_disk.time_created
        disk_dict['os_type'] = raw_disk.os_type
        disk_dict['hyper_vgeneration'] = raw_disk.hyper_vgeneration
        disk_dict['creation_data'] = raw_disk.creation_data
        disk_dict['disk_size_gb'] = raw_disk.disk_size_gb
        disk_dict['disk_size_bytes'] = raw_disk.disk_size_bytes
        disk_dict['unique_id'] = raw_disk.unique_id
        disk_dict['provisioning_state'] = raw_disk.provisioning_state
        disk_dict['disk_iops_read_write'] = raw_disk.disk_iops_read_write
        disk_dict['disk_mbps_read_write'] = raw_disk.disk_mbps_read_write
        disk_dict['disk_state'] = raw_disk.disk_state
        disk_dict['additional_properties'] = raw_disk.additional_properties

        disk_dict['encryption'] = raw_disk.encryption
        disk_dict['encryption_settings_collection'] = raw_disk.encryption_settings_collection
        if raw_disk.encryption_settings_collection and raw_disk.encryption_settings_collection.enabled:
            disk_dict['encryption_enabled'] = True
        else:
            disk_dict['encryption_enabled'] = False

        return disk_dict['id'], disk_dict

