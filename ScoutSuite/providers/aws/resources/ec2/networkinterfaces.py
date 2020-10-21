from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.core.console import print_exception


class NetworkInterfaces(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        super().__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_security_groups = await self.facade.ec2.get_network_interfaces(self.region, self.vpc)
        for raw_security_groups in raw_security_groups:
            try:
                name, resource = self._parse_network_interface(raw_security_groups)
                self[name] = resource
            except Exception as e:
                print_exception('Failed to parse {} resource: {}'.format(self.__class__.__name__, e))

    def _parse_network_interface(self, raw_network_interface):
        raw_network_interface['name'] = raw_network_interface['NetworkInterfaceId']
        raw_network_interface['arn'] = 'arn:aws:ec2:{}:{}:network-interface/{}'.format(self.region,
                                                                             raw_network_interface.get('OwnerId'),
                                                                             raw_network_interface.get('NetworkInterfaceId'))
        return raw_network_interface['NetworkInterfaceId'], raw_network_interface
