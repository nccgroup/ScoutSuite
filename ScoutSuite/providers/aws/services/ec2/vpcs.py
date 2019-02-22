from ScoutSuite.providers.aws.configs.regions_config import ScopedResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade
from ScoutSuite.providers.aws.services.ec2.instances import EC2Instances


class Vpcs(ScopedResources):
    def __init__(self):
        self.facade = AWSFacade()

    async def fetch_all(self, region):
        await super(Vpcs, self).fetch_all(region)

        for vpc in self:
            # TODO: Add vpc_resource_types
            instances = await EC2Instances(region).fetch_all(vpc)
            self[vpc]['instances'] = instances

        return self

    def parse_resource(self, vpc):
        return vpc['VpcId'], vpc

    async def get_resources_in_scope(self, region):
        return self.facade.ec2.get_vpcs(region)
