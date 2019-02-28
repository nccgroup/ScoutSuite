from ScoutSuite.providers.aws.resources.resources import AWSCompositeResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade
from ScoutSuite.providers.aws.services.ec2.instances import EC2Instances
from ScoutSuite.providers.aws.services.ec2.securitygroups import SecurityGroups
from ScoutSuite.providers.aws.services.ec2.networkinterfaces import NetworkInterfaces


class Vpcs(AWSCompositeResources):
    children = [
        (EC2Instances, 'instances'),
        (SecurityGroups, 'security_groups'),
        (NetworkInterfaces, 'network_interfaces')
    ]

    def __init__(self, scope):
        self.scope = scope
        self.facade = AWSFacade()

    async def fetch_all(self, **kwargs):
        await super(Vpcs, self).fetch_all()

        for vpc in self:
            scope = {'region': self.scope['region'], 'vpc': vpc}
            await self.fetch_children(self[vpc], scope=scope)

    def parse_resource(self, vpc):
        return vpc['VpcId'], {}

    async def get_resources_from_api(self):
        return self.facade.ec2.get_vpcs(self.scope['region'])
