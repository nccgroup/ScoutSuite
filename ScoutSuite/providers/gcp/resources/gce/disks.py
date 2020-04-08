from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.utils import get_non_provider_id


class Disks(Resources):
    def _parse_disk(self, raw_disk):
        disk_dict = {}
        disk_dict['id'] = get_non_provider_id(raw_disk['deviceName'])
        disk_dict['type'] = raw_disk.get('type')
        disk_dict['mode'] = raw_disk.get('mode')
        disk_dict['source_url'] = raw_disk.get('source')
        disk_dict['source_device_name'] = raw_disk.get('deviceName')
        disk_dict['bootable'] = raw_disk.get('boot')
        disk_dict['encrypted_with_csek'] = self._is_encrypted_with_csek(raw_disk)
        return disk_dict['id'], disk_dict

    def _is_encrypted_with_csek(self, raw_disk):
        return 'diskEncryptionKey' in raw_disk \
               and 'sha256' in raw_disk.get('diskEncryptionKey') \
               and raw_disk['diskEncryptionKey']['sha256'] != ''
