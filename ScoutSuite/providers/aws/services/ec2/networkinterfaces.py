from ScoutSuite.providers.aws.resources.resources import AWSResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade


class NetworkInterfaces(AWSResources):
    async def get_resources_from_api(self):
        return self.facade.ec2.get_network_interfaces(self.scope['region'], self.scope['vpc'])

    def parse_resource(self, raw_network_interace):
        raw_network_interace['name'] = raw_network_interace['NetworkInterfaceId']
        return raw_network_interace['NetworkInterfaceId'], raw_network_interace
