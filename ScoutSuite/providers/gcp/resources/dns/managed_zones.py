from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade


class ManagedZones(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_zones = await self.facade.dns.get_zones(self.project_id)
        for raw_zone in raw_zones.get('managedZones', []):
            zone_id, zone = self._parse_zone(raw_zone)
            self[zone_id] = zone

    def _parse_zone(self, raw_zone):
        zone_dict = {}
        zone_dict['id'] = raw_zone['id']
        zone_dict['name'] = raw_zone['name']
        zone_dict['description'] = self._get_description(raw_zone)
        zone_dict['dns_name'] = raw_zone['dnsName']
        zone_dict['name_servers'] = raw_zone.get('nameServers', None)
        zone_dict['visibility'] = raw_zone['visibility']
        zone_dict['creation_timestamp'] = raw_zone['creationTime']

        dnssec_config = raw_zone.get('dnssecConfig',None)
        if dnssec_config:
            zone_dict['dnssec_enabled'] = True if dnssec_config['state'] == 'on' else False
            zone_dict['dnssec_keys'] = self._get_keys(dnssec_config,zone_dict)
        else:
            zone_dict['dnssec_enabled'] = False
            zone_dict['dnssec_keys'] = None
            zone_dict['key_signing_algorithm'] = None
            zone_dict['zone_signing_algorithm']=None
        return zone_dict['id'], zone_dict

    def _get_description(self, raw_zone):
        description = raw_zone.get('description')
        return description if description else 'N/A'

    def _get_keys(self, dnssec_config,zone_dict):
        raw_keys = dnssec_config.get('defaultKeySpecs', None)
        if not raw_keys:
            return None
        key_dict = {}
        for raw_key in raw_keys:
            key_dict[raw_key['keyType']]={
                'key_type': raw_key['keyType'],
                'key_algorithm': raw_key['algorithm'],
                'length': raw_key['keyLength'],
            }
            if raw_key['keyType'] == 'keySigning':
                zone_dict['key_signing_algorithm'] = raw_key['algorithm']
            elif raw_key['keyType'] == 'zoneSigning':
                zone_dict['zone_signing_algorithm'] = raw_key['algorithm']



        return key_dict
