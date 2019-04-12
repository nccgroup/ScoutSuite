from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources


class Vpcs(AWSCompositeResources):
    """
    Fetches resources inside the virtual private clouds (VPCs) defined in a region. 
    :param add_ec2_classic: Setting this parameter to True will add 'EC2-Classic' to the list of VPCs.
    """

    def __init__(self, facade, scope: dict, add_ec2_classic=False):
        super(Vpcs, self).__init__(facade, scope)
        self.add_ec2_classic = add_ec2_classic

    async def fetch_all(self, **kwargs):
        raw_vpcs = await self.facade.ec2.get_vpcs(self.scope['region'])

        for raw_vpc in raw_vpcs:
            vpc_id, vpc = self._parse_vpc(raw_vpc)
            self[vpc_id] = vpc

        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={vpc_id: {'region': self.scope['region'], 'vpc': vpc_id}
                    for vpc_id in self}
        )

    def _parse_vpc(self, vpc):
        return vpc['VpcId'], {}
