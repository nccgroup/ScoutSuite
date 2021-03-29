from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade


class ManagedZones(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_zones = await self.facade.dns.get_zones(self.project_id)
        for raw_zone in raw_zones['managedZones']:
            zone_id,zone = self._parse_zone(raw_zone)
            self[zone_id] = zone

    def _parse_zone(self, raw_zone):
        zone_dict = {}
        zone_dict['id'] = raw_zone['id']
        zone_dict['name'] = raw_zone['name']
        zone_dict['description'] = raw_zone['description']
        zone_dict['dns_name'] = raw_zone['dnsName']
        zone_dict['name_servers'] = raw_zone.get('nameServers',None)
        zone_dict['visibility'] = raw_zone['visibility']
        zone_dict['creation_timestamp'] = raw_zone['creationTime']

        dnssec_config = raw_zone['dnssecConfig']
        zone_dict['dnssec_enabled'] = True if dnssec_config['state'] == 'on' else False
        zone_dict['dnssec_keys'] = dnssec_config.get('defaultKeySpecs',None)

        return zone_dict['id'], zone_dict


    def _get_description(self, raw_zone):
        description = raw_zone.get('description')
        return description if description else 'N/A'
