from ScoutSuite.providers.aws.resources.base import AWSResources


class NetworkInterfaces(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_security_groups = await self.facade.ec2.get_network_interfaces(self.scope['region'], self.scope['vpc'])
        for raw_security_groups in raw_security_groups:
            name, resource = self._parse_network_interface(raw_security_groups)
            self[name] = resource

    def _parse_network_interface(self, raw_network_interface):
        raw_network_interface['name'] = raw_network_interface['NetworkInterfaceId']
        return raw_network_interface['NetworkInterfaceId'], raw_network_interface
