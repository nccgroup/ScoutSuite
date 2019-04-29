from ScoutSuite.providers.gcp.resources.gce.disks import Disks


class InstanceDisks(Disks):
    def __init__(self, facade, instance):
        super(InstanceDisks, self).__init__(facade)
        self.instance = instance

    def fetch_all(self):
        raw_disks = self.instance.get('disks', {})
        for raw_disk in raw_disks:
            disk_id, disk = self._parse_disk(raw_disk)
            self[disk_id] = disk
        # We need self.instance to get the disks, but we do 
        # not want to have it in the generated JSON.
        del self.instance
