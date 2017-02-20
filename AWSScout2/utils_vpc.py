# Import opinel
from opinel.utils import *

# Import Scout2 tools
from AWSScout2.utils import *

########################################
##### VPC analysis functions
########################################



#
# Add a display name for all known CIDRs
#
known_cidrs = {'0.0.0.0/0': 'All'}
def put_cidr_name(aws_config, current_config, path, current_path, resource_id, callback_args):
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

#
# Read display name for CIDRs from ip-ranges files
#
aws_ip_ranges = read_ip_ranges(aws_ip_ranges_filename, False)
def get_cidr_name(cidr, ip_ranges_files, ip_ranges_name_key):
    for filename in ip_ranges_files:
        ip_ranges = read_ip_ranges(filename, local_file = True)
        for ip_range in ip_ranges:
            ip_prefix = netaddr.IPNetwork(ip_range['ip_prefix'])
            cidr = netaddr.IPNetwork(cidr)
            if cidr in ip_prefix:
                return ip_range[ip_ranges_name_key]
    for ip_range in aws_ip_ranges:
        ip_prefix = netaddr.IPNetwork(ip_range['ip_prefix'])
        cidr = netaddr.IPNetwork(cidr)
        if cidr in ip_prefix:
            return 'Unknown CIDR in %s %s' % (ip_range['service'], ip_range['region'])
    return 'Unknown CIDR'

#
# Propagate VPC names in VPC-related services (info only fetched during EC2 calls)
#
def propagate_vpc_names(aws_config, current_config, path, current_path, resource_id, callback_args):
    if resource_id == ec2_classic:
        current_config['name'] = ec2_classic
    else:
        target_path = copy.deepcopy(current_path)
        target_path[1] = 'ec2'
        target_path.append(resource_id)
        target_path.append('Name')
        target_path = '.'.join(target_path)
        current_config['name'] = get_value_at(aws_config, target_path, target_path)
