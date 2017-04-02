# -*- coding: utf-8 -*-
"""
Multi-service post-processing functions
"""

from opinel.utils import manage_dictionary, printInfo, printError, printException
from AWSScout2.utils import ec2_classic

from AWSScout2.configs.browser import get_object_at

import copy

def do_postprocessing(aws_config):
    match_instances_and_roles(aws_config)
    match_iam_policies_and_buckets(aws_config)
    vpc_postprocessing(aws_config)
    # final
    update_metadata(aws_config)







#
# Create dashboard metadata
#
def update_metadata(aws_config):
    # Security risks dropdown on a per-resource basis

    service_map = {}
    for service_group in aws_config['metadata']:
        for service in aws_config['metadata'][service_group]:
            if service not in aws_config['service_list']:
                continue
            if 'resources' not in aws_config['metadata'][service_group][service]:
                continue
            service_map[service] = service_group
    for s in aws_config['services']:
        if aws_config['services'][s] and 'violations' in aws_config['services'][s]:
            for v in aws_config['services'][s]['violations']:
                # Finding resource
                resource_path = aws_config['services'][s]['violations'][v]['display_path'] if 'display_path' in aws_config['services'][s]['violations'][v] else aws_config['services'][s]['violations'][v]['path']
                resource = resource_path.split('.')[-2]
                # h4ck...
                if resource == 'credential_report':
                    resource = resource_path.split('.')[-1].replace('>', '').replace('<', '')
                elif resource == s:
                    resource = resource_path.split('.')[-1]
                if aws_config['services'][s]['violations'][v]['flagged_items'] > 0:
                    try:
                        manage_dictionary(aws_config['metadata'][service_map[s]][s]['resources'][resource], 'risks', [])
                        aws_config['metadata'][service_map[s]][s]['resources'][resource]['risks'].append(v)
                    except Exception as e:
                        try:
                            manage_dictionary(aws_config['metadata'][service_map[s]][s]['summaries'][resource], 'risks', [])
                            aws_config['metadata'][service_map[s]][s]['summaries'][resource]['risks'].append(v)
                        except Exception as e:
                            printError('Service: %s' % s)
                            printError('Resource: %s' % resource)
                            printException(e)


########################################
# EC2 & IAM
########################################

def match_instances_and_roles(aws_config):
    """
    Foobar

    :param aws_config:
    """
    printInfo('Matching EC2 instances and IAM roles...')
    ec2_config = aws_config['services']['ec2']
    iam_config = aws_config['services']['iam']
    role_instances = {}
    for r in ec2_config['regions']:
        for v in ec2_config['regions'][r]['vpcs']:
            if 'instances' in ec2_config['regions'][r]['vpcs'][v]:
                for i in ec2_config['regions'][r]['vpcs'][v]['instances']:
                    instance_profile_id = ec2_config['regions'][r]['vpcs'][v]['instances'][i]['iam_instance_profile']['id'] if 'iam_instance_profile' in ec2_config['regions'][r]['vpcs'][v]['instances'][i] else None
                    if instance_profile_id:
                        manage_dictionary(role_instances, instance_profile_id, [])
                        role_instances[instance_profile_id].append(i)
    for role_id in iam_config['roles']:
        iam_config['roles'][role_id]['instances_count'] = 0
        for instance_profile_id in iam_config['roles'][role_id]['instance_profiles']:
            if instance_profile_id in role_instances:
                iam_config['roles'][role_id]['instance_profiles'][instance_profile_id]['instances'] = role_instances[instance_profile_id]
                iam_config['roles'][role_id]['instances_count'] += len(role_instances[instance_profile_id])



########################################
# S3 & IAM
########################################

def match_iam_policies_and_buckets(aws_config):
    printInfo('Matching S3 buckets and IAM policies...')
    s3_info = aws_config['services']['s3']
    iam_info = aws_config['services']['iam']
    if 'Action' in iam_info['permissions']:
        for action in (x for x in iam_info['permissions']['Action'] if ((x.startswith('s3:') and x != 's3:ListAllMyBuckets') or (x == '*'))):
            for iam_entity in iam_info['permissions']['Action'][action]:
                if 'Allow' in iam_info['permissions']['Action'][action][iam_entity]:
                    for allowed_iam_entity in iam_info['permissions']['Action'][action][iam_entity]['Allow']:
                        # For resource statements, we can easily rely on the existing permissions structure
                        if 'Resource' in iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]:
                            for full_path in (x for x in iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]['Resource'] if x.startswith('arn:aws:s3:') or x == '*'):
                                parts = full_path.split('/')
                                bucket_name = parts[0].split(':')[-1]
                                __update_iam_permissions(s3_info, bucket_name, iam_entity, allowed_iam_entity, iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]['Resource'][full_path])
                        # For notresource statements, we must fetch the policy document to determine which buckets are not protected
                        if 'NotResource' in iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]:
                            for full_path in (x for x in iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]['NotResource'] if x.startswith('arn:aws:s3:') or x == '*'):
                                for policy_type in ['InlinePolicies', 'ManagedPolicies']:
                                    if policy_type in iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]['NotResource'][full_path]:
                                        for policy in iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]['NotResource'][full_path][policy_type]:
                                            __update_bucket_permissions(s3_info, iam_info, action, iam_entity, allowed_iam_entity, full_path, policy_type, policy)

def __update_bucket_permissions(s3_info, iam_info, action, iam_entity, allowed_iam_entity, full_path, policy_type, policy_name):
    allowed_buckets = []
    # By default, all buckets are allowed
    for bucket_name in s3_info['buckets']:
        allowed_buckets.append(bucket_name)
    if policy_type == 'InlinePolicies':
        policy = iam_info[iam_entity.title()][allowed_iam_entity]['Policies'][policy_name]['PolicyDocument']
    elif policy_type == 'ManagedPolicies':
        policy = iam_info['ManagedPolicies'][policy_name]['PolicyDocument']
    else:
        printError('Error, found unknown policy type.')
    for statement in policy['Statement']:
        for target_path in statement['NotResource']:
            parts = target_path.split('/')
            bucket_name = parts[0].split(':')[-1]
            path = '/' + '/'.join(parts[1:]) if len(parts) > 1 else '/'
            if (path == '/' or path == '/*') and (bucket_name in allowed_buckets):
                # Remove bucket from list
                allowed_buckets.remove(bucket_name)
            elif bucket_name == '*':
                allowed_buckets = []
    policy_info = {}
    policy_info[policy_type] = {}
    policy_info[policy_type][policy_name] = iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]['NotResource'][full_path][policy_type][policy_name]
    for bucket_name in allowed_buckets:
        __update_iam_permissions(s3_info, bucket_name, iam_entity, allowed_iam_entity, policy_info)

def __update_iam_permissions(s3_info, bucket_name, iam_entity, allowed_iam_entity, policy_info):
    if bucket_name != '*' and bucket_name in s3_info['buckets']:
        bucket = s3_info['buckets'][bucket_name]
        manage_dictionary(bucket, iam_entity, {})
        manage_dictionary(bucket, iam_entity + '_count', 0)
        if not allowed_iam_entity in bucket[iam_entity]:
            bucket[iam_entity][allowed_iam_entity] = {}
            bucket[iam_entity + '_count'] = bucket[iam_entity + '_count'] + 1

        if 'inline_policies' in policy_info:
            manage_dictionary(bucket[iam_entity][allowed_iam_entity], 'inline_policies', {})
            bucket[iam_entity][allowed_iam_entity]['inline_policies'].update(policy_info['inline_policies'])
        if 'policies' in policy_info:
            manage_dictionary(bucket[iam_entity][allowed_iam_entity], 'policies', {})
            bucket[iam_entity][allowed_iam_entity]['policies'].update(policy_info['policies'])
    elif bucket_name == '*':
        for bucket in s3_info['buckets']:
            __update_iam_permissions(s3_info, bucket, iam_entity, allowed_iam_entity, policy_info)
        pass
    else:
        # Could be an error or cross-account access, ignore...
        pass



########################################
# VPC
########################################

def vpc_postprocessing(aws_config, ip_ranges = [], ip_ranges_name_key = None):
    printInfo('Post-processing VPC config...')
    # Security group usage: EC2 instances
    callback_args = {'status_path': [], 'sg_list_attribute_name': 'Groups', 'sg_id_attribute_name': 'GroupId'}
    go_to_and_do(aws_config, aws_config['services']['ec2'], ['regions', 'vpcs', 'instances', 'network_interfaces'], ['services', 'ec2'], list_resources_in_security_group, callback_args)
    # Security group usage: ELBs
    callback_args = {'status_path': ['Scheme'], 'sg_list_attribute_name': 'security_groups', 'sg_id_attribute_name': 'GroupId'}
    go_to_and_do(aws_config, aws_config['services']['ec2'], ['regions', 'vpcs', 'elbs'], ['services', 'ec2'], list_resources_in_security_group, callback_args)
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
    # Propagate VPC names outside EC2
    vpc_services = [ 'rds', 'redshift' ]
#    for service in vpc_services:
#        go_to_and_do(aws_config, aws_config['services'][service], ['regions', 'vpcs'], ['services', service], propagate_vpc_names, {})
    # Remove empty EC2-classic VPC placeholders
    go_to_and_do(aws_config, aws_config['services']['ec2'], ['regions'], ['services', 'ec2'], remove_empty_ec2_placeholders, {})


#
# Recursively go to a target and execute a callback
#
def go_to_and_do(aws_config, current_config, path, current_path, callback, callback_args = None):
  try:
    key = path.pop(0)
    if not current_config:
        current_config = aws_config
    if not current_path:
        current_path = []
    keys = key.split('.')
    if len(keys) > 1:
        while True:
            key = keys.pop(0)
            if not len(keys):
                break
            current_path.append(key)
            current_config = current_config[key]
    if key in current_config:
        current_path.append(key)
        for (i, value) in enumerate(current_config[key]):
            if len(path) == 0:
                if type(current_config[key] == dict) and type(value) != dict and type(value) != list:
                    callback(aws_config, current_config[key][value], path, current_path, value, callback_args)
                else:
                    # TODO: the current_config value passed here is not correct...
                    callback(aws_config, current_config, path, current_path, value, callback_args)
            else:
                tmp = copy.deepcopy(current_path)
                try:
                    tmp.append(value)
                    go_to_and_do(aws_config, current_config[key][value], copy.deepcopy(path), tmp, callback, callback_args)
                except:
                    tmp.pop()
                    tmp.append(i)
                    go_to_and_do(aws_config, current_config[key][i], copy.deepcopy(path), tmp, callback, callback_args)

  except Exception as e:
    printException(e)
    printInfo('Index: %s' % str(i))
    printInfo('Path: %s' % str(current_path))
#    printInfo('Config: %s' % str(current_config))
    printInfo('Key = %s' % str(key))
    printInfo('Value = %s' % str(value))
    printInfo('Path = %s' % path)


#
# EC2-Classic placeholders were automatically created - remove if empty after fetching all the data
#
def remove_empty_ec2_placeholders(aws_config, current_config, path, current_path, resource_id, callback_args):
    if ec2_classic in current_config and current_config['vpcs'][ec2_classic] == {}:
        current_config['vpcs'].pop(ec2_classic)




#
# List the resources associated with a given VPC security group (e.g. ec2 instances, redshift clusters, ...)
# TODO: fix it when single region is fetched but more region data exist...
#
def list_resources_in_security_group(aws_config, current_config, path, current_path, resource_id, callback_args):
    # Retrieve service and resource type from current path
    service = current_path[1]
    resource_type = current_path[-1]
    # Get resource
    resource_path = copy.deepcopy(current_path)
    resource_path.append(resource_id)
    resource = get_object_at(aws_config, resource_path)
    if 'status_path' in callback_args:
        resource_status = get_object_at(resource, callback_args['status_path'])
    else:
        resource_status = None
    # Get list of VPC security groups for the resource
    # TODO: create EC2 classic SG and see how it differs from a VPC SG ... same for RDS Etc...
    sg_base_path = copy.deepcopy(current_path)
    sg_base_path.pop()
    sg_base_path[1] = 'ec2'
    #sg_base_path.append(callback_args)
    sg_base_path.append('security_groups')
    # Issue 89 & 91 : can instances have no security group?
    try:
      for resource_sg in resource[callback_args['sg_list_attribute_name']]:
        # Get security group
        sg_path = copy.deepcopy(sg_base_path)
        sg_path.append(resource_sg[callback_args['sg_id_attribute_name']])
        print('SG path: %s' % sg_path)
        sg = get_object_at(aws_config, sg_path)
        # Add usage information
        manage_dictionary(sg, 'used_by', {})
        manage_dictionary(sg['used_by'], service, {})
        manage_dictionary(sg['used_by'][service], 'resource_type', {})
        manage_dictionary(sg['used_by'][service]['resource_type'], resource_type, {} if resource_status else [])
        if resource_status:
            manage_dictionary(sg['used_by'][service]['resource_type'][resource_type], resource_status, [])
            if not resource_id in sg['used_by'][service]['resource_type'][resource_type][resource_status]:
                sg['used_by'][service]['resource_type'][resource_type][resource_status].append(resource_id)
        else:
                sg['used_by'][service]['resource_type'][resource_type].append(resource_id)
    except Exception as e:
        region = current_path[3]
        vpc_id = current_path[5]
        if vpc_id == ec2_classic and resource_type == 'elbs':
            pass
        else:
            printError('Failed to parse %s in %s in %s' % (resource_type, vpc_id, region))
            printException(e)
