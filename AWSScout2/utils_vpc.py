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
def analyze_vpc_config(aws_config):
    printInfo('Analyzing VPC config...')
    # Security group usage: EC2 instances
    callback_args = {'resource_type': 'ec2_instances', 'status_path': ['State', 'Name'], 'sg_list_attribute_name': 'security_groups', 'sg_id_attribute_name': 'GroupId'}
    go_to_and_do(aws_config, aws_config['services']['ec2'], ['regions', 'vpcs', 'instances'], ['services', 'ec2'], list_resources_in_security_group, callback_args)
    # Security group usage: Redshift clusters
    callback_args = {'resource_type': 'redshift_clusters', 'status_path': ['ClusterStatus'], 'sg_list_attribute_name': 'VpcSecurityGroups', 'sg_id_attribute_name': 'VpcSecurityGroupId'}
    go_to_and_do(aws_config, aws_config['services']['redshift'], ['regions', 'vpcs', 'clusters'], ['services', 'redshift'], list_resources_in_security_group, callback_args)
    # Security group usage: RDS instances
    callback_args = {'resource_type': 'rds_instances', 'status_path': ['DBInstanceStatus'], 'sg_list_attribute_name': 'VpcSecurityGroups', 'sg_id_attribute_name': 'VpcSecurityGroupId'}
    go_to_and_do(aws_config, aws_config['services']['rds'], ['regions', 'vpcs', 'instances'], ['services', 'rds'], list_resources_in_security_group, callback_args)


#
# List the resources associated with a given VPC security group (e.g. ec2 instances, redshift clusters, ...)
#
def list_resources_in_security_group(aws_config, current_config, path, current_path, resource_id, callback_args):
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
        manage_dictionary(sg['used_by'], callback_args['resource_type'], {})
        manage_dictionary(sg['used_by'][callback_args['resource_type']], resource_status, [])
        if not resource_id in sg['used_by'][callback_args['resource_type']][resource_status]:
            sg['used_by'][callback_args['resource_type']][resource_status].append(resource_id)

#
# Get arbitrary object given a dictionary and path (list of keys)
#
def get_object_at(dictionary, path, attribute_name = None):
    o = dictionary
    for p in path:
        o = o[p]
    if attribute_name:
        return o[attribute_name]
    else:
        return o
