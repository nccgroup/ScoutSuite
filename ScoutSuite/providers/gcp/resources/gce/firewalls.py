from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.core.console import print_exception


class Firewalls(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_firewalls = await self.facade.gce.get_firewalls(self.project_id)
        parsing_error_counter = 0
        for raw_firewall in raw_firewalls:
            try:
                firewall_id, firewall = self._parse_firewall(raw_firewall)
                self[firewall_id] = firewall
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_firewall(self, raw_firewall):
        firewall_dict = {}
        firewall_dict['id'] = raw_firewall['id']
        firewall_dict['project_id'] = raw_firewall['selfLink'].split('/')[-4]
        firewall_dict['name'] = raw_firewall['name']
        firewall_dict['description'] = self._get_description(raw_firewall)
        firewall_dict['creation_timestamp'] = raw_firewall['creationTimestamp']
        firewall_dict['network'] = raw_firewall['network'].split('/')[-1]
        firewall_dict['network_url'] = raw_firewall['network']
        firewall_dict['priority'] = raw_firewall['priority']
        firewall_dict['source_ranges'] = raw_firewall.get('sourceRanges', [])
        firewall_dict['destination_ranges'] = raw_firewall.get('destinationRanges', [])
        firewall_dict['source_tags'] = raw_firewall.get('sourceTags', [])
        firewall_dict['target_tags'] = raw_firewall.get('targetTags', [])
        firewall_dict['direction'] = raw_firewall['direction']
        firewall_dict['disabled'] = raw_firewall['disabled']
        firewall_dict['logs'] = raw_firewall['logConfig'].get('enable', False)

        self._parse_firewall_rules(firewall_dict, raw_firewall)
        return firewall_dict['id'], firewall_dict

    def _parse_firewall_rules(self, firewall_dict, raw_firewall):
        for direction in ['allowed', 'denied']:
            direction_string = '%s_traffic' % direction
            firewall_dict[direction_string] = {
                'tcp': [],
                'udp': [],
                'icmp': []
            }
            if direction in raw_firewall:
                firewall_dict['action'] = direction
                for rule in raw_firewall[direction]:
                    if rule['IPProtocol'] not in firewall_dict[direction_string]:
                        firewall_dict[direction_string][rule['IPProtocol']] = ['*']
                    else:
                        if rule['IPProtocol'] == 'all':
                            for protocol in firewall_dict[direction_string]:
                                firewall_dict[direction_string][protocol] = ['0-65535']
                            break
                        else:
                            if firewall_dict[direction_string][rule['IPProtocol']] != ['0-65535']:
                                if 'ports' in rule:
                                    firewall_dict[direction_string][rule['IPProtocol']] += rule['ports']
                                else:
                                    firewall_dict[direction_string][rule['IPProtocol']] = ['0-65535']

    def _get_description(self, raw_firewall):
        description = raw_firewall.get('description')
        return description if description else 'N/A'
