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
        parsing_error_counter = 0
        for raw_security_groups in raw_security_groups:
            try:
                name, resource = self._parse_network_interface(raw_security_groups)
                self[name] = resource
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_network_interface(self, raw_network_interface):
        raw_network_interface['name'] = raw_network_interface['NetworkInterfaceId']
        raw_network_interface['arn'] = 'arn:aws:ec2:{}:{}:network-interface/{}'.format(self.region,
                                                                             raw_network_interface.get('OwnerId'),
                                                                             raw_network_interface.get('NetworkInterfaceId'))
        return raw_network_interface['NetworkInterfaceId'], raw_network_interface
