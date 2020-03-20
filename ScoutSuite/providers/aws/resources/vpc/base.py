import netaddr

from ScoutSuite.core.fs import read_ip_ranges
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions

from .flow_logs import FlowLogs
from .vpcs import RegionalVpcs
from .peering_connections import PeeringConnections

known_cidrs = {'0.0.0.0/0': 'All'}
aws_ip_ranges = {}


class VPC(Regions):
    _children = [
        (RegionalVpcs, 'vpcs'),
        (FlowLogs, 'flow_logs'),
        (PeeringConnections, 'peering_connections'),
    ]

    def __init__(self, facade: AWSFacade):
        # VPC is not a real service but a subset of ec2:
        super(VPC, self).__init__('ec2', facade)


# TODO: move these helpers elsewhere:


def put_cidr_name(current_config, path, current_path, resource_id, callback_args):
    """Add a display name for all known CIDRs."""

    if 'cidrs' in current_config:
        cidr_list = []
        for cidr in current_config['cidrs']:
            if type(cidr) == dict:
                cidr = cidr['CIDR']
            if cidr in known_cidrs:
                cidr_name = known_cidrs[cidr]
            else:
                cidr_name = get_cidr_name(
                    cidr, callback_args['ip_ranges'], callback_args['ip_ranges_name_key'])
                known_cidrs[cidr] = cidr_name
            cidr_list.append({'CIDR': cidr, 'CIDRName': cidr_name})
        current_config['cidrs'] = cidr_list


def get_cidr_name(cidr, ip_ranges_files, ip_ranges_name_key):
    """Read display name for CIDRs from ip-ranges files."""

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
