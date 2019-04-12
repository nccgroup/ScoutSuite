from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.gcp.resources.projects import Projects

class Snapshots(Resources):
    def __init__(self, gcp_facade, project_id):
        self.gcp_facade = gcp_facade
        self.project_id = project_id

    async def fetch_all(self):
        raw_snapshots = await self.gcp_facade.gce.get_snapshots(self.project_id)
        for raw_snapshot in raw_snapshots:
            snapshot_id, snapshot = self._parse_snapshot(raw_snapshot)
            self[snapshot_id] = snapshot

    def _parse_snapshot(self, raw_snapshot):
        snapshot_dict = {}
        snapshot_dict['id'] = raw_snapshot['id']
        snapshot_dict['name'] = raw_snapshot['name']
        snapshot_dict['description'] = self._get_description(raw_snapshot)
        snapshot_dict['creation_timestamp'] = raw_snapshot['creationTimestamp']
        snapshot_dict['status'] = raw_snapshot['status']
        snapshot_dict['source_disk_id'] = raw_snapshot['sourceDiskId']
        snapshot_dict['source_disk_url'] = raw_snapshot['sourceDisk']
        return snapshot_dict['id'], snapshot_dict

    def _get_description(self, raw_snapshot):
        description = raw_snapshot.get('description')   
        return description if description else 'N/A'
