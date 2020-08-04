from ScoutSuite.providers.osc.resources.base import OSCResources
from ScoutSuite.providers.osc.facade.base import OSCFacade
from ScoutSuite.utils import manage_dictionary

import logging

class Snapshots(OSCResources):
    def __init__(self, facade: OSCFacade, region: str, vpc: str = None):
        super(Snapshots, self).__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        try:
            raw_snapshots = await self.facade.api.get_snapshots(self.region)
            for raw_snapshots in raw_snapshots:
                name, resource = self._parse_snapshots(raw_snapshots)
                self[name] = resource
                print(name)
                print(resource)
        except Exception as e:
            logging.getLogger("scout").critical(f"OSC ::: Snapshots _fecth_all() Exception {e}\n\n\n")

    def _parse_snapshots(self, raw_snapshot):
        snapshot = {}
        snapshot['id'] = raw_snapshot['SnapshotId']
        snapshot['description'] = raw_snapshot['Description']
        snapshot['account_id'] = raw_snapshot['AccountId']
        snapshot['state'] = raw_snapshot['State']
        snapshot['volume_id'] = raw_snapshot['VolumeId']
        if 'Tags' in raw_snapshot:
            for tag in raw_snapshot['Tags']:
                if tag["Key"] == "Name":
                    snapshot['name'] = ["Value"]
        snapshot['rules'] = {'ingress': {}, 'egress': {}}
        ingress_protocols, ingress_rules_count = self._parse_snapshot_rules(
            raw_snapshot)
        snapshot['rules']['ingress']['volumes'] = ingress_protocols
        snapshot['rules']['ingress']['count'] = ingress_rules_count
        egress_protocols, egress_rules_count = self._parse_snapshot_rules(raw_snapshot)
        snapshot['rules']['egress']['volumes'] = egress_protocols
        snapshot['rules']['egress']['count'] = egress_rules_count
        return snapshot['id'], snapshot

    def _parse_snapshot_rules(self, rule):
        snapshots = {}
        rules_count = 0
        snapshot_id = rule["SnapshotId"] if "SnapshotId" in rule else "EMPTY"
        snapshots = manage_dictionary(snapshots, snapshot_id, {})
        snapshots[snapshot_id] = manage_dictionary(snapshots[snapshot_id], 'volume', {})
        rules_count += 1
        volume_id = "NO VOLUME"
        if "VolumeId" in rule:
            volume_id = rule["VolumeId"]
        manage_dictionary(snapshots[snapshot_id]['volume'], volume_id, {})
        return snapshots, rules_count