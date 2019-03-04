from ScoutSuite.providers.aws.resources.resources import AWSResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade


class NetworkInterfaces(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_security_groups = self.facade.ec2.get_network_interfaces(self.scope['region'], self.scope['vpc'])
        for raw_security_groups in raw_security_groups:
            name, resource = self._parse_network_interface(raw_security_groups)
            self[name] = resource

    def _parse_network_interface(self, raw_network_interace):
        raw_network_interace['name'] = raw_network_interace['NetworkInterfaceId']
        return raw_network_interace['NetworkInterfaceId'], raw_network_interace
