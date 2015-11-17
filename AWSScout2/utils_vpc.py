# Import opinel
from opinel.utils import *

# Import Scout2 tools
from AWSScout2.utils import *

########################################
##### VPC analysis functions
########################################

#
# VPC-level analysis
#
def analyze_vpc_config(aws_config, ip_ranges, ip_ranges_name_key):
    printInfo('Analyzing VPC config...')
    # Security group usage: EC2 instances
    callback_args = {'status_path': ['State', 'Name'], 'sg_list_attribute_name': 'security_groups', 'sg_id_attribute_name': 'GroupId'}
    go_to_and_do(aws_config, aws_config['services']['ec2'], ['regions', 'vpcs', 'instances'], ['services', 'ec2'], list_resources_in_security_group, callback_args)
    # Security group usage: Redshift clusters
    callback_args = {'status_path': ['ClusterStatus'], 'sg_list_attribute_name': 'VpcSecurityGroups', 'sg_id_attribute_name': 'VpcSecurityGroupId'}
    go_to_and_do(aws_config, aws_config['services']['redshift'], ['regions', 'vpcs', 'clusters'], ['services', 'redshift'], list_resources_in_security_group, callback_args)
    # Security group usage: RDS instances
    callback_args = {'status_path': ['DBInstanceStatus'], 'sg_list_attribute_name': 'VpcSecurityGroups', 'sg_id_attribute_name': 'VpcSecurityGroupId'}
    go_to_and_do(aws_config, aws_config['services']['rds'], ['regions', 'vpcs', 'instances'], ['services', 'rds'], list_resources_in_security_group, callback_args)
    # Add friendly name for CIDRs
    if len(ip_ranges):
        callback_args = {'ip_ranges': ip_ranges, 'ip_ranges_name_key': ip_ranges_name_key}
        go_to_and_do(aws_config, aws_config['services']['ec2'], ['regions', 'vpcs', 'security_groups', 'rules', 'protocols', 'ports'], ['services', 'ec2'], put_cidr_name, callback_args)

#
# List the resources associated with a given VPC security group (e.g. ec2 instances, redshift clusters, ...)
#
def list_resources_in_security_group(aws_config, current_config, path, current_path, resource_id, callback_args):
    # Retrieve service and resource type from current path
    service = current_path[1]
    resource_type = current_path[-1]
    # Get resource
    resource_path = copy.deepcopy(current_path)
    resource_path.append(resource_id)
    resource = get_object_at(aws_config, resource_path)
    resource_status = get_object_at(resource, callback_args['status_path'])
    # Get list of VPC security groups for the resource
    sg_base_path = copy.deepcopy(current_path)
    sg_base_path.pop()
    sg_base_path[1] = 'ec2'
    sg_base_path.append('security_groups')
    for resource_sg in resource[callback_args['sg_list_attribute_name']]:
        # Get security group
        sg_path = copy.deepcopy(sg_base_path)
        sg_path.append(resource_sg[callback_args['sg_id_attribute_name']])
        sg = get_object_at(aws_config, sg_path)
        # Add usage information
        manage_dictionary(sg, 'used_by', {})
        manage_dictionary(sg['used_by'], service, {})
        manage_dictionary(sg['used_by'][service], 'resource_type', {})
        manage_dictionary(sg['used_by'][service]['resource_type'], resource_type, {})
        manage_dictionary(sg['used_by'][service]['resource_type'][resource_type], resource_status, [])
        if not resource_id in sg['used_by'][service]['resource_type'][resource_type][resource_status]:
            sg['used_by'][service]['resource_type'][resource_type][resource_status].append(resource_id)

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
                cidr_name = get_cidr_name(cidr, callback_args['ip_ranges'], callback_args['ip_ranges_name_key'][0])
                known_cidrs[cidr] = cidr_name
            cidr_list.append({'CIDR': cidr, 'CIDRName': cidr_name})
        current_config['cidrs'] = cidr_list

#
# Read display name for CIDRs from ip-ranges files
#
def get_cidr_name(cidr, ip_ranges_files, ip_ranges_name_key):
    for filename in ip_ranges_files:
        ip_ranges = read_ip_ranges(filename, local_file = True)
        for ip_range in ip_ranges:
            ip_prefix = netaddr.IPNetwork(ip_range['ip_prefix'])
            cidr = netaddr.IPNetwork(cidr)
            if cidr in ip_prefix:
                return ip_range[ip_ranges_name_key]
    return 'Unknown CIDR'
