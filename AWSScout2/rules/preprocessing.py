# -*- coding: utf-8 -*-

import copy

from opinel.utils.console import printError, printException, printInfo
from opinel.utils.globals import manage_dictionary

from AWSScout2.configs.browser import combine_paths, get_object_at, get_value_at
from AWSScout2.utils import ec2_classic
from AWSScout2.services.vpc import put_cidr_name



def preprocessing(aws_config, ip_ranges = [], ip_ranges_name_key = None):
    """
    Tweak the AWS config to match cross-service resources and clean any fetching artifacts

    :param aws_config:
    :return:
    """
    set_aws_account_id(aws_config)
    sort_vpc_flow_logs(aws_config['services']['vpc'])
    sort_elbs(aws_config)
    list_ec2_network_attack_surface(aws_config['services']['ec2'])
    add_security_group_name_to_ec2_grants(aws_config['services']['ec2'], aws_config['aws_account_id'])
    match_instances_and_roles(aws_config)
    match_roles_and_cloudformation_stacks(aws_config)
    match_roles_and_vpc_flowlogs(aws_config)
    match_iam_policies_and_buckets(aws_config)
    match_security_groups_and_resources(aws_config)
    add_cidr_display_name(aws_config, ip_ranges, ip_ranges_name_key)
    merge_route53_and_route53domains(aws_config)



def add_cidr_display_name(aws_config, ip_ranges, ip_ranges_name_key):
    if len(ip_ranges):
        callback_args = {'ip_ranges': ip_ranges, 'ip_ranges_name_key': ip_ranges_name_key}
        go_to_and_do(aws_config, aws_config['services']['ec2'], ['regions', 'vpcs', 'security_groups', 'rules', 'protocols', 'ports'], ['services', 'ec2'], put_cidr_name, callback_args)


def add_security_group_name_to_ec2_grants(ec2_config, aws_account_id):
    """
    Github issue #24: display the security group names in the list of grants (added here to have ligher JS code)

    :param ec2_config:
    :param aws_account_id:
    :return:
    """
    go_to_and_do(ec2_config, None, ['regions', 'vpcs', 'security_groups', 'rules', 'protocols', 'ports', 'security_groups'], [], add_security_group_name_to_ec2_grants_callback, {'AWSAccountId': aws_account_id})


def add_security_group_name_to_ec2_grants_callback(ec2_config, current_config, path, current_path, ec2_grant, callback_args):
    sg_id = ec2_grant['GroupId']
    if sg_id in current_path:
        target = current_path[:(current_path.index(sg_id) + 1)]
        ec2_grant['GroupName'] = get_value_at(ec2_config, target, 'name')
    elif ec2_grant['UserId'] == callback_args['AWSAccountId']:
        if 'VpcId' in ec2_grant:
            target = current_path[:(current_path.index('vpcs') + 1)]
            target.append(ec2_grant['VpcId'])
            target.append('security_groups')
            target.append(sg_id)
        else:
            target = current_path[:(current_path.index('security_groups') + 1)]
            target.append(sg_id)
        ec2_grant['GroupName'] = get_value_at(ec2_config, target, 'name')


def list_ec2_network_attack_surface(ec2_config):
    go_to_and_do(ec2_config, None, ['regions', 'vpcs', 'instances', 'network_interfaces', 'PrivateIpAddresses'], [], list_ec2_network_attack_surface_callback, {})


def list_ec2_network_attack_surface_callback(ec2_config, current_config, path, current_path, privateip_id, callback_args):
    if 'Association' in current_config and current_config['Association']:
        public_ip = current_config['Association']['PublicIp']
        manage_dictionary(ec2_config, 'attack_surface', {})
        manage_dictionary(ec2_config['attack_surface'], public_ip, {'protocols': {}})
        for sg_info in current_config['Groups']:
            sg_id = sg_info['GroupId']
            sg_path = copy.deepcopy(current_path[0:4])
            sg_path.append('security_groups')
            sg_path.append(sg_id)
            sg_path.append('rules')
            sg_path.append('ingress')
            ingress_rules = get_object_at(ec2_config, sg_path)
            public_ip_grants = {}
            for p in ingress_rules['protocols']:
                for port in ingress_rules['protocols'][p]['ports']:
                    if 'cidrs' in ingress_rules['protocols'][p]['ports'][port]:
                        manage_dictionary(public_ip_grants, 'protocols', {})
                        manage_dictionary(public_ip_grants['protocols'], p, {'ports': {}})
                        manage_dictionary(public_ip_grants['protocols'][p]['ports'], port, {'cidrs': []})
                        public_ip_grants['protocols'][p]['ports'][port]['cidrs'] += ingress_rules['protocols'][p]['ports'][port]['cidrs']
            ec2_config['attack_surface'][public_ip]['protocols'].update(public_ip_grants)


def match_iam_policies_and_buckets(aws_config):
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


def match_roles_and_cloudformation_stacks(aws_config):
    go_to_and_do(aws_config, aws_config['services']['cloudformation'], ['regions', 'stacks'], [], match_roles_and_cloudformation_stacks_callback, {})


def match_roles_and_cloudformation_stacks_callback(aws_config, current_config, path, current_path, stack_id, callback_args):
    if 'RoleARN' not in current_config:
        return
    role_arn = current_config.pop('RoleARN')
    current_config['iam_role'] = __get_role_info(aws_config, 'arn', role_arn)


def match_roles_and_vpc_flowlogs(aws_config):
    go_to_and_do(aws_config, aws_config['services']['vpc'], ['regions', 'flow_logs'], [], match_roles_and_vpc_flowlogs_callback, {})


def match_roles_and_vpc_flowlogs_callback(aws_config, current_config, path, current_path, flowlog_id, callback_args):
    if 'DeliverLogsPermissionArn' not in current_config:
        return
    delivery_role_arn = current_config.pop('DeliverLogsPermissionArn')
    current_config['delivery_role'] = __get_role_info(aws_config, 'arn', delivery_role_arn)


def __get_role_info(aws_config, attribute_name, attribute_value):
    iam_role_info = {'name': None, 'id': None}
    for role_id in aws_config['services']['iam']['roles']:
        if aws_config['services']['iam']['roles'][role_id][attribute_name] == attribute_value:
            iam_role_info['name'] = aws_config['services']['iam']['roles'][role_id]['name']
            iam_role_info['id'] = role_id
            break
    return iam_role_info


def match_security_groups_and_resources(aws_config):
    # EC2 instances
    callback_args = {'status_path': [ '..', '..', 'State', 'Name' ], 'resource_id_path': ['..'], 'sg_list_attribute_name': 'Groups', 'sg_id_attribute_name': 'GroupId'}
    go_to_and_do(aws_config, aws_config['services']['ec2'], ['regions', 'vpcs', 'instances', 'network_interfaces'], ['services', 'ec2'], match_security_groups_and_resources_callback, callback_args)
    # ELBs
    #callback_args = {'status_path': ['Scheme'], 'sg_list_attribute_name': 'security_groups',                     'sg_id_attribute_name': 'GroupId'}
    # go_to_and_do(aws_config, aws_config['services']['ec2'], ['regions', 'vpcs', 'elbs'], ['services', 'ec2'], list_resources_in_security_group, callback_args)
    # Redshift clusters
    callback_args = {'status_path': ['ClusterStatus'], 'sg_list_attribute_name': 'VpcSecurityGroups', 'sg_id_attribute_name': 'VpcSecurityGroupId'}
    go_to_and_do(aws_config, aws_config['services']['redshift'], ['regions', 'vpcs', 'clusters'], ['services', 'redshift'], match_security_groups_and_resources_callback, callback_args)
    # RDS instances
    callback_args = {'status_path': ['DBInstanceStatus'], 'sg_list_attribute_name': 'VpcSecurityGroups', 'sg_id_attribute_name': 'VpcSecurityGroupId'}
    go_to_and_do(aws_config, aws_config['services']['rds'], ['regions', 'vpcs', 'instances'], ['services', 'rds'], match_security_groups_and_resources_callback, callback_args)


def match_security_groups_and_resources_callback(aws_config, current_config, path, current_path, resource_id, callback_args):
    service = current_path[1]
    original_resource_path = combine_paths(copy.deepcopy(current_path), [ resource_id ])
    resource = get_object_at(aws_config, original_resource_path)
    if not 'resource_id_path' in callback_args:
        resource_type = current_path[-1]
        resource_path = copy.deepcopy(current_path)
        resource_path.append(resource_id)
    else:
        resource_path = combine_paths(copy.deepcopy(current_path), callback_args['resource_id_path'])
        resource_id = resource_path[-1]
        resource_type = resource_path[-2]
    #print('Resource path: %s' % resource_path)
    #print('Resource type: %s' % resource_type)
    #print('Resource id: %s' % resource_id)
    if 'status_path' in callback_args:
        status_path = combine_paths(copy.deepcopy(original_resource_path), callback_args['status_path'])
        #print('Status path: %s' % status_path)
        resource_status = get_object_at(aws_config, status_path)
    else:
        resource_status = None
    sg_base_path = copy.deepcopy(current_path[0:6])
    sg_base_path[1] = 'ec2'
    sg_base_path.append('security_groups')
    # Issue 89 & 91 : can instances have no security group?
    try:
        for resource_sg in resource[callback_args['sg_list_attribute_name']]:
            sg_id = resource_sg[callback_args['sg_id_attribute_name']]
            sg_path = copy.deepcopy(sg_base_path)
            sg_path.append(sg_id)
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


def merge_route53_and_route53domains(aws_config):
    if 'route53domains' not in aws_config['services']:
        return
    aws_config['services']['route53'].update(aws_config['services']['route53domains'])
    aws_config['services'].pop('route53domains')


def set_aws_account_id(aws_config):
    for rt in ['groups', 'policies', 'roles', 'users']:
        for r in aws_config['services']['iam'][rt]:
            if 'aws_account_id' not in aws_config or aws_config['aws_account_id'] == None:
                if 'arn' in aws_config['services']['iam'][rt][r]:
                    aws_config['aws_account_id'] = aws_config['services']['iam'][rt][r]['arn'].split(':')[4]
        if 'aws_account_id' in aws_config and aws_config['aws_account_id'] != None:
            break
    if 'aws_account_id' not in aws_config:
        aws_config['aws_account_id'] = None


def sort_vpc_flow_logs(vpc_config):
    go_to_and_do(vpc_config, None, ['regions', 'flow_logs'], [], sort_vpc_flow_logs_callback, {})


def sort_elbs(aws_config):
    """
    ELB and ELBv2 are different services, but for consistency w/ the console move them to the EC2 config

    :param aws_config:
    :return:
    """
    if 'elb' in aws_config['services']:
        go_to_and_do(aws_config, aws_config['services']['elb'], ['regions', 'vpcs', 'elbs'], [], sort_elbs_callback, {})
        aws_config['services'].pop('elb')
    if 'elbv2' in aws_config['services']:
        go_to_and_do(aws_config, aws_config['services']['elbv2'], ['regions', 'vpcs', 'elbs'], [], sort_elbs_callback, {})
        aws_config['services'].pop('elbv2')


def sort_elbs_callback(aws_config, current_config, path, current_path, elb_id, callback_args):
    vpc_config = get_object_at(aws_config, ['services', 'ec2'] + current_path[:-1])
    manage_dictionary(vpc_config, 'elbs', {})
    vpc_config['elbs'][elb_id] = current_config



def sort_vpc_flow_logs_callback(vpc_config, current_config, path, current_path, flow_log_id, callback_args):
    attached_resource = current_config['ResourceId']
    if attached_resource.startswith('vpc-'):
        vpc_path = combine_paths(current_path[0:2], ['vpcs', attached_resource])
        attached_vpc = get_object_at(vpc_config, vpc_path)
        manage_dictionary(attached_vpc, 'flow_logs', [])
        if flow_log_id not in attached_vpc['flow_logs']:
            attached_vpc['flow_logs'].append(flow_log_id)
        for subnet_id in attached_vpc['subnets']:
            manage_dictionary(attached_vpc['subnets'][subnet_id], 'flow_logs', [])
            if flow_log_id not in attached_vpc['subnets'][subnet_id]['flow_logs']:
                attached_vpc['subnets'][subnet_id]['flow_logs'].append(flow_log_id)
    elif attached_resource.startswith('subnet-'):
        all_vpcs = get_object_at(vpc_config, combine_paths(current_path[0:2], ['vpcs']))
        for vpc in all_vpcs:
            if attached_resource in all_vpcs[vpc]['subnets']:
                manage_dictionary(all_vpcs[vpc]['subnets'][attached_resource], 'flow_logs', [])
                if flow_log_id not in all_vpcs[vpc]['subnets'][attached_resource]['flow_logs']:
                    all_vpcs[vpc]['subnets'][attached_resource]['flow_logs'].append(flow_log_id)
                break
    else:
        printError('Resource %s attached to flow logs is not handled' % attached_resource)


def go_to_and_do(aws_config, current_config, path, current_path, callback, callback_args = None):
    """
    Recursively go to a target and execute a callback

    :param aws_config:                  A
    :param current_config:
    :param path:
    :param current_path:
    :param callback:
    :param callback_args:
    :return:
    """
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
            for (i, value) in enumerate(list(current_config[key])):
                if len(path) == 0:
                    if type(current_config[key] == dict) and type(value) != dict and type(value) != list:
                        callback(aws_config, current_config[key][value], path, current_path, value, callback_args)
                    else:
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
        printInfo('Key = %s' % str(key))
        printInfo('Value = %s' % str(value))
        printInfo('Path = %s' % path)
