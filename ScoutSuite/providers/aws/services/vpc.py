# -*- coding: utf-8 -*-

import netaddr
import copy

from opinel.utils.aws import get_name
from opinel.utils.globals import manage_dictionary
from opinel.utils.fs import load_data, read_ip_ranges

from ScoutSuite.providers.base.configs.browser import get_value_at
from ScoutSuite.utils import ec2_classic, get_keys
from ScoutSuite.providers.aws.configs.regions import RegionalServiceConfig, RegionConfig
from ScoutSuite.providers.aws.configs.vpc import VPCConfig as SingleVPCConfig

########################################
# Globals
########################################

protocols_dict = load_data('protocols.json', 'protocols')

########################################
# VPCRegionConfig
########################################


class VPCRegionConfig(RegionConfig):
    """
    VPC configuration for a single AWS region
    """

    def parse_customer_gateway(self, global_params, region, cgw):
        cgw['id'] = cgw.pop('CustomerGatewayId')
        self.customer_gateways[cgw['id']] = cgw

    def parse_flow_log(self, global_params, region, flow_log):
        """

        :param global_params:
        :param region:
        :param flow_log:
        :return:
        """
        get_name(flow_log, flow_log, 'FlowLogId')
        flow_log_id = flow_log.pop('FlowLogId')
        self.flow_logs[flow_log_id] = flow_log

    def parse_network_acl(self, global_params, region, network_acl):
        """

        :param global_params:
        :param region:
        :param network_acl:
        :return:
        """
        vpc_id = network_acl['VpcId']
        network_acl['id'] = network_acl.pop('NetworkAclId')
        get_name(network_acl, network_acl, 'id')
        manage_dictionary(network_acl, 'rules', {})
        network_acl['rules']['ingress'] = self.__parse_network_acl_entries(network_acl['Entries'], False)
        network_acl['rules']['egress'] = self.__parse_network_acl_entries(network_acl['Entries'], True)
        network_acl.pop('Entries')
        # Save
        manage_dictionary(self.vpcs, vpc_id, SingleVPCConfig(self.vpc_resource_types))
        self.vpcs[vpc_id].network_acls[network_acl['id']] = network_acl

    def __parse_network_acl_entries(self, entries, egress):
        """

        :param entries:
        :param egress:
        :return:
        """
        acl_dict = {}
        for entry in entries:
            if entry['Egress'] == egress:
                acl = {}
                for key in ['RuleAction', 'RuleNumber']:
                    acl[key] = entry[key]
                acl['CidrBlock'] = entry['CidrBlock'] if 'CidrBlock' in entry else entry['Ipv6CidrBlock']
                acl['protocol'] = protocols_dict[entry['Protocol']]
                if 'PortRange' in entry:
                    from_port = entry['PortRange']['From'] if entry['PortRange']['From'] else 1
                    to_port = entry['PortRange']['To'] if entry['PortRange']['To'] else 65535
                    acl['port_range'] = from_port if from_port == to_port else str(from_port) + '-' + str(to_port)
                else:
                    acl['port_range'] = '1-65535'

                acl_dict[acl.pop('RuleNumber')] = acl
        return acl_dict

    def parse_route_table(self, global_params, region, rt):
        route_table = {}
        vpc_id = rt['VpcId']
        get_name(rt, route_table, 'VpcId')  # TODO: change get_name to have src then dst
        get_keys(rt, route_table, ['Routes', 'Associations', 'PropagatingVgws'])
        # Save
        manage_dictionary(self.vpcs, vpc_id, SingleVPCConfig(self.vpc_resource_types))
        self.vpcs[vpc_id].route_tables[rt['RouteTableId']] = route_table

    def parse_subnet(self, global_params, region, subnet):
        """
        Parse subnet object.

        :param global_params:
        :param region:
        :param subnet:
        :return:
        """
        vpc_id = subnet['VpcId']
        manage_dictionary(self.vpcs, vpc_id, SingleVPCConfig(self.vpc_resource_types))
        subnet_id = subnet['SubnetId']
        get_name(subnet, subnet, 'SubnetId')
        # set flow logs that cover this subnet
        subnet['flow_logs'] = get_subnet_flow_logs_list(self, subnet)
        # Save
        manage_dictionary(self.vpcs, vpc_id, SingleVPCConfig(self.vpc_resource_types))
        self.vpcs[vpc_id].subnets[subnet_id] = subnet

    def parse_vpc(self, global_params, region_name, vpc):
        """

        :param global_params:
        :param region_name:
        :param vpc:
        :return:
        """
        vpc_id = vpc['VpcId']
        # Save
        manage_dictionary(self.vpcs, vpc_id, SingleVPCConfig(self.vpc_resource_types))
        self.vpcs[vpc_id].name = get_name(vpc, {}, 'VpcId')

    def parse_vpn_connection(self, global_params, region_name, vpnc):
        vpnc['id'] = vpnc.pop('VpnConnectionId')
        self.vpn_connections[vpnc['id']] = vpnc

    def parse_vpn_gateway(self, global_params, region_name, vpng):
        vpng['id'] = vpng.pop('VpnGatewayId')
        self.vpn_gateways[vpng['id']] = vpng


########################################
# VPCConfig
########################################


class VPCConfig(RegionalServiceConfig):
    """
    VPC configuration for all AWS regions
    """

    region_config_class = VPCRegionConfig

    def __init__(self, service_metadata, thread_config):
        super(VPCConfig, self).__init__(service_metadata, thread_config)


########################################
##### VPC analysis functions
########################################

known_cidrs = {'0.0.0.0/0': 'All'}

def put_cidr_name(aws_config, current_config, path, current_path, resource_id, callback_args):
    """
    Add a display name for all known CIDRs
    :param aws_config:
    :param current_config:
    :param path:
    :param current_path:
    :param resource_id:
    :param callback_args:
    :return:
    """
    if 'cidrs' in current_config:
        cidr_list = []
        for cidr in current_config['cidrs']:
            if type(cidr) == dict:
                cidr = cidr['CIDR']
            if cidr in known_cidrs:
                cidr_name = known_cidrs[cidr]
            else:
                cidr_name = get_cidr_name(cidr, callback_args['ip_ranges'], callback_args['ip_ranges_name_key'])
                known_cidrs[cidr] = cidr_name
            cidr_list.append({'CIDR': cidr, 'CIDRName': cidr_name})
        current_config['cidrs'] = cidr_list


aws_ip_ranges = {}  # read_ip_ranges(aws_ip_ranges_filename, False)

def get_cidr_name(cidr, ip_ranges_files, ip_ranges_name_key):
    """
    Read display name for CIDRs from ip-ranges files
    :param cidr:
    :param ip_ranges_files:
    :param ip_ranges_name_key:
    :return:
    """
    for filename in ip_ranges_files:
        ip_ranges = read_ip_ranges(filename, local_file=True)
        for ip_range in ip_ranges:
            ip_prefix = netaddr.IPNetwork(ip_range['ip_prefix'])
            cidr = netaddr.IPNetwork(cidr)
            if cidr in ip_prefix:
                return ip_range[ip_ranges_name_key].strip()
    for ip_range in aws_ip_ranges:
        ip_prefix = netaddr.IPNetwork(ip_range['ip_prefix'])
        cidr = netaddr.IPNetwork(cidr)
        if cidr in ip_prefix:
            return 'Unknown CIDR in %s %s' % (ip_range['service'], ip_range['region'])
    return 'Unknown CIDR'

def propagate_vpc_names(aws_config, current_config, path, current_path, resource_id, callback_args):
    """
    Propagate VPC names in VPC-related services (info only fetched during EC2 calls)
    :param aws_config:
    :param current_config:
    :param path:
    :param current_path:
    :param resource_id:
    :param callback_args:
    :return:
    """
    if resource_id == ec2_classic:
        current_config['name'] = ec2_classic
    else:
        target_path = copy.deepcopy(current_path)
        target_path[1] = 'ec2'
        target_path.append(resource_id)
        target_path.append('Name')
        target_path = '.'.join(target_path)
        current_config['name'] = get_value_at(aws_config, target_path, target_path)

def get_subnet_flow_logs_list(current_config, subnet):
    """
    Return the flow logs that cover a given subnet

    :param current_config:
    :param subnet: the subnet that the flow logs should cover
    :return:
    """
    flow_logs_list = []
    for flow_log in current_config.flow_logs:
        if current_config.flow_logs[flow_log]['ResourceId'] == subnet['SubnetId'] or \
                current_config.flow_logs[flow_log]['ResourceId'] == subnet['VpcId']:
            flow_logs_list.append(flow_log)
    return flow_logs_list
