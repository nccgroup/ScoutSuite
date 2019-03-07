import asyncio

from ScoutSuite.providers.aws.resources.resources import AWSCompositeResources
from ScoutSuite.providers.aws.resources.ec2.instances import EC2Instances
from ScoutSuite.providers.aws.resources.ec2.securitygroups import SecurityGroups
from ScoutSuite.providers.aws.resources.ec2.networkinterfaces import NetworkInterfaces


class Vpcs(AWSCompositeResources):
    _children = [
        (EC2Instances, 'instances'),
        (SecurityGroups, 'security_groups'),
        (NetworkInterfaces, 'network_interfaces')
    ]

    async def fetch_all(self, **kwargs):
        vpcs = await self.facade.ec2.get_vpcs(self.scope['region'])
        for vpc in vpcs:
            name, resource = self._parse_vpc(vpc)
            self[name] = resource

        # TODO: make a refactoring of the following:
        if len(self) == 0:
            return
        tasks = {
            asyncio.ensure_future(
                self._fetch_children(
                    self[vpc],
                    {'region': self.scope['region'], 'vpc': vpc}
                )
            ) for vpc in self
        }
        await asyncio.wait(tasks)

    def _parse_vpc(self, vpc):
        return vpc['VpcId'], {}

