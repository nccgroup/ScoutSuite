from ScoutSuite.providers.aws.resources.base import AWSCompositeResources


class Vpcs(AWSCompositeResources):
    """
    Fetches resources inside the virtual private clouds (VPCs) defined in a region. 
    :param add_ec2_classic: Setting this parameter to True will add 'EC2-Classic' to the list of VPCs.
    """

    def __init__(self, facade, region: str, add_ec2_classic=False):
        super(Vpcs, self).__init__(facade)
        self.region = region
        self.add_ec2_classic = add_ec2_classic

    async def fetch_all(self):
        raw_vpcs = await self.facade.ec2.get_vpcs(self.region)

        for raw_vpc in raw_vpcs:
            vpc_id, vpc = self._parse_vpc(raw_vpc)
            self[vpc_id] = vpc

        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={vpc_id: {'region': self.region, 'vpc': vpc_id}
                    for vpc_id in self}
        )

    def _parse_vpc(self, raw_vpc):
        vpc = {}
        vpc['id'] = raw_vpc['VpcId']
        vpc['cidr_block'] = raw_vpc['CidrBlock']
        vpc['default'] = raw_vpc['IsDefault']
        vpc['state'] = raw_vpc['State']

        # pull the name from tags
        name_tag = next((d for i, d in enumerate(raw_vpc.get('Tags', [])) if d.get('Key') == 'Name'), None)
        if name_tag:
            vpc['name'] = name_tag.get('Value')
        else:
            vpc['name'] = raw_vpc['VpcId']

        return vpc['id'], vpc
