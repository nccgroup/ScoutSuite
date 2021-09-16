from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.utils import format_arn


class NetworkInterfaces(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        super().__init__(facade)
        self.region = region
        self.vpc = vpc
        self.partition = facade.partition
        self.service = 'ec2'
        self.resource_type = 'network-interface'

    async def fetch_all(self):
        raw_security_groups = await self.facade.ec2.get_network_interfaces(self.region, self.vpc)
        for raw_security_groups in raw_security_groups:
            name, resource = self._parse_network_interface(raw_security_groups)
            self[name] = resource

    def _parse_network_interface(self, raw_network_interface):
        raw_network_interface['name'] = raw_network_interface['NetworkInterfaceId']
        raw_network_interface['arn'] = format_arn(self.partition, self.service, self.region, raw_network_interface.get('OwnerId'), raw_network_interface.get('NetworkInterfaceId'), self.resource_type)
        return raw_network_interface['NetworkInterfaceId'], raw_network_interface
