from ScoutSuite.providers.aliyun.resources.base import AliyunResources
from ScoutSuite.providers.aliyun.facade.base import AliyunFacade


class VPCs(AliyunResources):
    def __init__(self, facade: AliyunFacade, region: str):
        super(VPCs, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        for raw_vpc in await self.facade.vpc.get_vpcs(region=self.region):
            id, vpc = self._parse_vpcs(raw_vpc)
            self[id] = vpc

    def _parse_vpcs(self, raw_vpc):
        vpc_dict = {}
        vpc_dict['id'] = raw_vpc.get('VpcId')

        if raw_vpc.get('VpcName') == '':
            vpc_dict['name'] = raw_vpc.get('VpcId')
        else:
            vpc_dict['name'] = raw_vpc.get('VpcName')

        vpc_dict['vrouter_id'] = raw_vpc.get('VRouterId')
        vpc_dict['vswitch_ids'] = raw_vpc.get('VSwitchIds')
        vpc_dict['description'] = raw_vpc.get('Description')
        vpc_dict['status'] = raw_vpc.get('Status')
        vpc_dict['nat_gateway_ids'] = raw_vpc.get('NatGatewayIds')
        vpc_dict['user_cidrs'] = raw_vpc.get('UserCidrs')
        vpc_dict['ipv6_cidr_block'] = raw_vpc.get('Ipv6CidrBlock')
        vpc_dict['region_id'] = raw_vpc.get('RegionId')
        vpc_dict['network_acl_num'] = raw_vpc.get('NetworkAclNum')
        vpc_dict['creation_time'] = raw_vpc.get('CreationTime')
        vpc_dict['router_table_ids'] = raw_vpc.get('RouterTableIds')
        vpc_dict['resource_group_id'] = raw_vpc.get('ResourceGroupId')
        vpc_dict['cen_status'] = raw_vpc.get('CenStatus')
        vpc_dict['cidr_block'] = raw_vpc.get('CidrBlock')
        vpc_dict['is_default'] = raw_vpc.get('IsDefault')

        return vpc_dict['id'], vpc_dict
