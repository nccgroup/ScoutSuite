from ScoutSuite.providers.osc.resources.base import OSCResources
from ScoutSuite.providers.osc.facade.base import OSCFacade
from ScoutSuite.utils import manage_dictionary

import logging


class Volumes(OSCResources):
    def __init__(self, facade: OSCFacade, region: str, vpc: str = None):
        super(Volumes, self).__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self, regions=None, excluded_regions=None, partition_name='osc', **kwargs):
        try:
            raw_volumes = await self.facade.api.get_volumes()
            for raw_volume in raw_volumes:
                name, resource = self._parse_volumes(raw_volume)
                self[name] = resource
                #print(resource)
        except Exception as e:
            logging.warning(e)

    def _parse_volumes(self, raw_volume):
        volume = {}
        volume['size'] = raw_volume['Size']
        volume['id'] = raw_volume['VolumeId']
        volume['type'] = raw_volume['VolumeType']
        volume['volume_id'] = raw_volume["SnapshotId"] if "SnapshotId" in raw_volume else ""
        volume['state'] = raw_volume['State']
        volume["rules"] = {'ingress': {}, 'egress': {}}
        
        ingress_volumes, ingress_rules_count = self._parse_volume_rules(
            volume)
        volume['rules']['ingress']['volumes'] = ingress_volumes
        volume['rules']['ingress']['count'] = ingress_rules_count
        egress_volumes, egress_rules_count = self._parse_volume_rules(
            volume)
        volume['rules']['egress']['volumes'] = egress_volumes
        volume['rules']['egress']['count'] = egress_rules_count
        return volume['id'], volume

    def _parse_volume_rules(self, rules):
        volumes = {}
        rules_count = 0
        for rule in rules:
            volume_id = rule["SnapshotId"] if "SnapshotId" in rule else None
            if volume_id is None:
                volume_id = "EMPTY"
            volumes = manage_dictionary(volumes, volume_id, {})
            volumes[volume_id] = manage_dictionary(
                volumes[volume_id], 'volumes', {})
            rules_count += 1

        return volumes, rules_count
