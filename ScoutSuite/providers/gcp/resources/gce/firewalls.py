from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade


class Firewalls(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_firewalls = await self.facade.gce.get_firewalls(self.project_id)
        for raw_firewall in raw_firewalls:
            firewall_id, firewall = self._parse_firewall(raw_firewall)
            self[firewall_id] = firewall

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
                'udp': []
            }
            if direction in raw_firewall:
                firewall_dict['action'] = direction
                for rule in raw_firewall[direction]:
                    # everything
                    if rule['IPProtocol'] == 'all':
                        firewall_dict[direction_string]["tcp"] = ['0-65535']
                        firewall_dict[direction_string]["udp"] = ['0-65535']
                        firewall_dict[direction_string]["icmp"] = ['Portless Protocol']
                    # protocols that do not support ports
                    elif rule['IPProtocol'] not in firewall_dict[direction_string]:
                        # only including ICMP
                        if rule['IPProtocol'] == 'icmp':
                            firewall_dict[direction_string]["icmp"] = ['Portless Protocol']
                        else:
                            pass
                    # protocols that support ports
                    else:
                        if firewall_dict[direction_string][rule['IPProtocol']] != ['0-65535']:
                            if 'ports' in rule:
                                firewall_dict[direction_string][rule['IPProtocol']] += rule['ports']
                            else:
                                firewall_dict[direction_string][rule['IPProtocol']] = ['0-65535']
                # remove empty values
                firewall_dict[direction_string] = {k: v for k, v in firewall_dict[direction_string].items() if v}

    def _get_description(self, raw_firewall):
        description = raw_firewall.get('description')
        return description if description else 'N/A'
