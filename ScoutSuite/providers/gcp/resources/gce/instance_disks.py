from ScoutSuite.providers.gcp.resources.gce.disks import Disks
from ScoutSuite.core.console import print_exception


class InstanceDisks(Disks):
    def __init__(self, facade, instance):
        super().__init__(facade)
        self.instance = instance

    def fetch_all(self):
        raw_disks = self.instance.get('disks', {})
        parsing_error_counter = 0
        for raw_disk in raw_disks:
            try:
                disk_id, disk = self._parse_disk(raw_disk)
                self[disk_id] = disk
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))
        # We need self.instance to get the disks, but we do 
        # not want to have it in the generated JSON.
        del self.instance
