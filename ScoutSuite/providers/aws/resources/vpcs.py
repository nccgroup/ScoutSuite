import asyncio

from ScoutSuite.providers.aws.resources.resources import AWSCompositeResources


class Vpcs(AWSCompositeResources):
    """
    Fetches resources inside the virtual private clouds (VPCs) defined in a region. 
    :param add_ec2_classic: Setting this parameter to True will add 'EC2-Classic' to the list of VPCs.
    """

    def __init__(self, facade, scope: dict, add_ec2_classic=False):
        super(Vpcs, self).__init__(facade, scope)
        self.add_ec2_classic = add_ec2_classic

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
                self._fetch_children(self[vpc], {'region': self.scope['region'], 'vpc': vpc})
            ) for vpc in self
        }

        await asyncio.wait(tasks)

    def _parse_vpc(self, vpc):
        return vpc['VpcId'], {}
