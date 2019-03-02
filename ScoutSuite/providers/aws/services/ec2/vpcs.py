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

    async def fetch_all(self, **kwargs):
        vpcs = self.facade.ec2.get_vpcs(self.scope['region'])
        for vpc in vpcs:
            name, resource = self._parse_vpc(vpc)
            self[name] = resource

        for vpc in self:
            scope = {'region': self.scope['region'], 'vpc': vpc}
            await self._fetch_children(self[vpc], scope=scope)

    def _parse_vpc(self, vpc):
        return vpc['VpcId'], {}

