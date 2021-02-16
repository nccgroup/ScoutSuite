from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.core.console import print_exception


class Networks(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_networks = await self.facade.gce.get_networks(self.project_id)
        parsing_error_counter = 0
        for raw_network in raw_networks:
            try:
                network_id, network = self._parse_network(raw_network)
                self[network_id] = network
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_network(self, raw_network):
        network_dict = {}
        network_dict['id'] = raw_network['id']
        network_dict['project_id'] = raw_network['selfLink'].split('/')[-4]
        network_dict['name'] = raw_network['name']
        network_dict['description'] = self._get_description(raw_network)
        network_dict['creation_timestamp'] = raw_network['creationTimestamp']
        network_dict['auto_subnet'] = raw_network.get('autoCreateSubnetworks', None)
        network_dict['routing_config'] = raw_network['routingConfig']

        network_dict['network_url'] = raw_network['selfLink']
        network_dict['subnetwork_urls'] = raw_network.get('subnetworks', None)

        return network_dict['id'], network_dict

    def _get_description(self, raw_network):
        description = raw_network.get('description')
        return description if description else 'N/A'
