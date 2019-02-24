from ScoutSuite.providers.aws.configs.regions_config import ScopedResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade


class NetworkInterfaces(ScopedResources):
    # TODO: The init could take a "scope" dictionary containing the necessary info. In this case, the owner_id and the region
    def __init__(self, region):
        self.region = region
        self.facade = AWSFacade()

    async def get_resources_in_scope(self, vpc):
        return self.facade.ec2.get_network_interfaces(self.region, vpc)

    def parse_resource(self, raw_network_interace):
        raw_network_interace['name'] = raw_network_interace['NetworkInterfaceId']
        return raw_network_interace['NetworkInterfaceId'], raw_network_interace
