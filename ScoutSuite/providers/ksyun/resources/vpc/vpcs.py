from ScoutSuite.providers.ksyun.facade.base import KsyunFacade
from ScoutSuite.providers.ksyun.resources.base import KsyunResources


class VPCs(KsyunResources):
    def __init__(self, facade: KsyunFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_vpcs = await self.facade.vpc.get_vpcs(region=self.region)
        if raw_vpcs:
            for raw_vpc in raw_vpcs:
                id, vpc = self._parse_vpcs(raw_vpc)
                self[id] = vpc

    def _parse_vpcs(self, raw_vpc):
        vpc_dict = {}
        vpc_dict['id'] = raw_vpc.get('VpcId')

        if raw_vpc.get('VpcName') == '':
            vpc_dict['name'] = raw_vpc.get('VpcId')
        else:
            vpc_dict['name'] = raw_vpc.get('VpcName')
        vpc_dict['region_id'] = self.region
        vpc_dict['creation_time'] = raw_vpc.get('CreateTime')
        vpc_dict['cidr_block'] = raw_vpc.get('CidrBlock')
        vpc_dict['is_default'] = raw_vpc.get('IsDefault')

        # vpc_dict['vrouter_id'] = raw_vpc.get('VRouterId')
        # vpc_dict['vswitch_ids'] = raw_vpc.get('VSwitchIds')
        # vpc_dict['description'] = raw_vpc.get('Description')
        # vpc_dict['status'] = raw_vpc.get('Status')
        # vpc_dict['nat_gateway_ids'] = raw_vpc.get('NatGatewayIds')
        # vpc_dict['user_cidrs'] = raw_vpc.get('UserCidrs')
        # vpc_dict['ipv6_cidr_block'] = raw_vpc.get('Ipv6CidrBlock')
        # vpc_dict['network_acl_num'] = raw_vpc.get('NetworkAclNum')
        # vpc_dict['router_table_ids'] = raw_vpc.get('RouterTableIds')
        # vpc_dict['resource_group_id'] = raw_vpc.get('ResourceGroupId')
        # vpc_dict['cen_status'] = raw_vpc.get('CenStatus')

        return vpc_dict['id'], vpc_dict
