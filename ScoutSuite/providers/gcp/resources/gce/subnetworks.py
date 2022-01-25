from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade


class Subnetworks(Resources):
    def __init__(self, facade: GCPFacade, project_id: str, region: str):
        super().__init__(facade)
        self.project_id = project_id
        self.region = region

    async def fetch_all(self):
        raw_subnetworks = await self.facade.gce.get_subnetworks(self.project_id, self.region)
        for raw_subnetwork in raw_subnetworks:
            subnetwork_id, subnetwork = self._parse_subnetwork(raw_subnetwork)
            self[subnetwork_id] = subnetwork

    def _parse_subnetwork(self, raw_subnetwork):
        subnetwork_dict = {}
        subnetwork_dict['id'] = raw_subnetwork['id']
        subnetwork_dict['project_id'] = raw_subnetwork['selfLink'].split('/')[-5]
        subnetwork_dict['region'] = raw_subnetwork['region'].split('/')[-1]
        subnetwork_dict['name'] = "{}-{}".format(raw_subnetwork['name'], subnetwork_dict['region'])
        subnetwork_dict['gateway_address'] = raw_subnetwork['gatewayAddress']
        subnetwork_dict['ip_range'] = raw_subnetwork['ipCidrRange']
        subnetwork_dict['creation_timestamp'] = raw_subnetwork['creationTimestamp']
        subnetwork_dict['private_ip_google_access'] = raw_subnetwork['privateIpGoogleAccess']

        subnetwork_dict['subnetwork_url'] = raw_subnetwork['selfLink']
        subnetwork_dict['network_url'] = raw_subnetwork['network']

        if 'logConfig' in raw_subnetwork:
            subnetwork_dict['flowlogs_enabled'] = raw_subnetwork['logConfig']['enable']
        else:
            # Set as UNKNOWN for now. For instance, some projects' 
            # default networks with flow logs enabled do not have a logConfig 
            # stanza in JSON output.
            subnetwork_dict['flowlogs_enabled'] = "UNKNOWN"

        return subnetwork_dict['id'], subnetwork_dict
