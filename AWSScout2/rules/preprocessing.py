# -*- coding: utf-8 -*-

import copy

from opinel.utils.console import printDebug, printError, printException, printInfo
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
    map_all_sgs(aws_config)
    map_all_subnets(aws_config)
    set_emr_vpc_ids(aws_config)
    sort_vpc_flow_logs(aws_config['services']['vpc'])
    #parse_elb_policies(aws_config)
    list_ec2_network_attack_surface(aws_config['services']['ec2'])
    add_security_group_name_to_ec2_grants(aws_config['services']['ec2'], aws_config['aws_account_id'])
    process_cloudtrail_trails(aws_config['services']['cloudtrail'])
    process_network_acls(aws_config['services']['vpc'])
    match_network_acls_and_subnets(aws_config['services']['vpc'])
    match_instances_and_subnets(aws_config)
    match_instances_and_roles(aws_config)
    match_roles_and_cloudformation_stacks(aws_config)
    match_roles_and_vpc_flowlogs(aws_config)
    match_iam_policies_and_buckets(aws_config)
    match_security_groups_and_resources(aws_config)
    process_vpc_peering_connections(aws_config)
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


def process_cloudtrail_trails(cloudtrail_config):
    printInfo('Processing CloudTrail config...')
    global_events_logging = []
    for region in cloudtrail_config['regions']:
        for trail_id in cloudtrail_config['regions'][region]['trails']:
            trail = cloudtrail_config['regions'][region]['trails'][trail_id]
            if 'HomeRegion' in trail and trail['HomeRegion'] != region:
                # Part of a multi-region trail, skip until we find the whole object
                continue
            if trail['IncludeGlobalServiceEvents'] == True and trail['IsLogging'] == True:
                global_events_logging.append((region, trail_id,))
    cloudtrail_config['IncludeGlobalServiceEvents'] = False if (len(global_events_logging) == 0) else True
    cloudtrail_config['DuplicatedGlobalServiceEvents'] = True if (len(global_events_logging) > 1) else False


def process_network_acls(vpc_config):
    printInfo('Analyzing VPC Network ACLs...')
    go_to_and_do(vpc_config, None, ['regions', 'vpcs', 'network_acls'], [], process_network_acls_callback, {})


def process_network_acls_callback(vpc_config, current_config, path, current_path, privateip_id, callback_args):
    # Check if the network ACL allows all traffic from all IP addresses
    process_network_acls_check_for_allow_all(current_config, 'ingress')
    process_network_acls_check_for_allow_all(current_config, 'egress')
    # Check if the network ACL only has the default rules
    process_network_acls_check_for_aws_default(current_config, 'ingress')
    process_network_acls_check_for_aws_default(current_config, 'egress')


def process_network_acls_check_for_allow_all(network_acl, direction):
    network_acl['allow_all_%s_traffic' % direction] = 0
    for rule_number in network_acl['rules'][direction]:
        rule = network_acl['rules'][direction][rule_number]
        if rule['RuleAction'] == 'deny':
            # If a deny rule appears before an allow all, do not raise the flag
            break
        if (rule['CidrBlock'] == '0.0.0.0/0') and (rule['RuleAction'] == 'allow') and (rule['port_range'] == '1-65535') and (rule['protocol'] == 'ALL'):
                network_acl['allow_all_%s_traffic' % direction] = rule_number
                break


def process_network_acls_check_for_aws_default(network_acl, direction):
    if len(network_acl['rules'][direction]) == 2 and int(network_acl['allow_all_%s_traffic' % direction]) > 0 and '100' in network_acl['rules'][direction]:
        # Assume it is AWS' default rules because there are 2 rules (100 and 65535) and the first rule allows all traffic
        network_acl['use_default_%s_rules' % direction] = True
    else:
        network_acl['use_default_%s_rules' % direction] = False


def list_ec2_network_attack_surface(ec2_config):
    ec2_config['attack_surface'] = {}
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
                        manage_dictionary(ec2_config['attack_surface'][public_ip]['protocols'], p, {'ports': {}})
                        manage_dictionary(ec2_config['attack_surface'][public_ip]['protocols'][p]['ports'], port, {'cidrs': []})
                        ec2_config['attack_surface'][public_ip]['protocols'][p]['ports'][port]['cidrs'] += ingress_rules['protocols'][p]['ports'][port]['cidrs']


sg_map = {}
def map_all_sgs(aws_config):
    go_to_and_do(aws_config, aws_config['services']['ec2'], ['regions', 'vpcs', 'security_groups'], ['services', 'ec2'], map_resource, {'map': sg_map})


subnet_map = {}
def map_all_subnets(aws_config):
    go_to_and_do(aws_config, aws_config['services']['vpc'], ['regions', 'vpcs', 'subnets'], ['services', 'vpc'], map_resource, {'map': subnet_map})


def map_resource(ec2_config, current_config, path, current_path, resource_id, callback_args):
    map = callback_args['map']
    if resource_id not in map:
        map[resource_id] = {'region': current_path[3]}
        if len(current_path) > 5:
            map[resource_id]['vpc_id'] = current_path[5]


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


def match_network_acls_and_subnets(vpc_config):
    printInfo('Matching VPC network ACLs and subnets...')
    go_to_and_do(vpc_config, vpc_config, ['regions', 'vpcs', 'network_acls'], [], match_network_acls_and_subnets_callback, {})


def match_network_acls_and_subnets_callback(vpc_config, current_config, path, current_path, acl_id, callback_args):
    for association in current_config['Associations']:
        subnet_path = current_path[:-1] + ['subnets', association['SubnetId']]
        subnet = get_object_at(vpc_config, subnet_path)
        subnet['network_acl'] = acl_id


def match_instances_and_subnets(aws_config):
    go_to_and_do(aws_config, aws_config['services']['ec2'], ['regions', 'vpcs', 'instances'], [], match_instances_and_subnets_callback, {})


def match_instances_and_subnets_callback(aws_config, current_config, path, current_path, instance_id, callback_args):
    subnet_id = current_config['SubnetId']
    vpc = subnet_map[subnet_id]
    subnet = aws_config['services']['vpc']['regions'][vpc['region']]['vpcs'][vpc['vpc_id']]['subnets'][subnet_id]
    manage_dictionary(subnet, 'instances', [])
    if instance_id not in subnet['instances']:
        subnet['instances'].append(instance_id)


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
                    instance_profile = ec2_config['regions'][r]['vpcs'][v]['instances'][i]['IamInstanceProfile']
                    instance_profile_id = instance_profile['Id'] if instance_profile else None
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


def process_vpc_peering_connections(aws_config):
    go_to_and_do(aws_config, aws_config['services']['vpc'], ['regions', 'peering_connections'], [], process_vpc_peering_connections_callback, {})


def process_vpc_peering_connections_callback(aws_config, current_config, path, current_path, pc_id, callback_args):

    # Create a list of peering connection IDs in each VPC
    info = 'AccepterVpcInfo' if current_config['AccepterVpcInfo']['OwnerId'] == aws_config['aws_account_id'] else 'RequesterVpcInfo'
    region = current_path[1]
    vpc_id = current_config[info]['VpcId']
    target = aws_config['services']['vpc']['regions'][region]['vpcs'][vpc_id]
    manage_dictionary(target, 'peering_connections', [])
    if pc_id not in target['peering_connections']:
        target['peering_connections'].append(pc_id)

    # VPC information for the peer'd VPC
    current_config['peer_info'] = copy.deepcopy(current_config['AccepterVpcInfo' if info == 'RequesterVpcInfo' else 'RequesterVpcInfo'])
    if 'PeeringOptions' in current_config['peer_info']:
        current_config['peer_info'].pop('PeeringOptions')
    if 'organization' in aws_config and current_config['peer_info']['OwnerId'] in aws_config['organization']:
        current_config['peer_info']['name'] = aws_config['organization'][current_config['peer_info']['OwnerId']]['Name']
    else:
        current_config['peer_info']['name'] = current_config['peer_info']['OwnerId']



def match_security_groups_and_resources(aws_config):
    if aws_config['services']['ec2']['regions'] == {}:
        return
    # EC2 instances
    callback_args = {'status_path': [ '..', '..', 'State', 'Name' ], 'resource_id_path': ['..'], 'sg_list_attribute_name': ['Groups'], 'sg_id_attribute_name': 'GroupId'}
    go_to_and_do(aws_config, aws_config['services']['ec2'], ['regions', 'vpcs', 'instances', 'network_interfaces'], ['services', 'ec2'], match_security_groups_and_resources_callback, callback_args)
    # EFS
    callback_args = {'status_path': ['LifeCycleState'], 'sg_list_attribute_name': ['security_groups']}
    go_to_and_do(aws_config, aws_config['services']['efs'], ['regions', 'file_systems', 'mount_targets'], ['services', 'efs'], match_security_groups_and_resources_callback, callback_args)
    # ELBs
    callback_args = {'status_path': ['Scheme'], 'sg_list_attribute_name': ['security_groups'], 'sg_id_attribute_name': 'GroupId'}
    go_to_and_do(aws_config, aws_config['services']['ec2'], ['regions', 'vpcs', 'elbs'], ['services', 'ec2'], match_security_groups_and_resources_callback, callback_args)
    callback_args = {'status_path': ['State', 'Code'], 'sg_list_attribute_name': ['security_groups'], 'sg_id_attribute_name': 'GroupId'}
    go_to_and_do(aws_config, aws_config['services']['elbv2'], ['regions', 'vpcs', 'lbs'], ['services', 'elbv2'], match_security_groups_and_resources_callback, callback_args)
    # Redshift clusters
    callback_args = {'status_path': ['ClusterStatus'], 'sg_list_attribute_name': ['VpcSecurityGroups'], 'sg_id_attribute_name': 'VpcSecurityGroupId'}
    go_to_and_do(aws_config, aws_config['services']['redshift'], ['regions', 'vpcs', 'clusters'], ['services', 'redshift'], match_security_groups_and_resources_callback, callback_args)
    # RDS instances
    callback_args = {'status_path': ['DBInstanceStatus'], 'sg_list_attribute_name': ['VpcSecurityGroups'], 'sg_id_attribute_name': 'VpcSecurityGroupId'}
    go_to_and_do(aws_config, aws_config['services']['rds'], ['regions', 'vpcs', 'instances'], ['services', 'rds'], match_security_groups_and_resources_callback, callback_args)
    # ElastiCache clusters
    callback_args = {'status_path': ['CacheClusterStatus'], 'sg_list_attribute_name': ['SecurityGroups'], 'sg_id_attribute_name': 'SecurityGroupId'}
    go_to_and_do(aws_config, aws_config['services']['elasticache'], ['regions', 'vpcs', 'clusters'], ['services', 'elasticache'], match_security_groups_and_resources_callback, callback_args)
    # EMR clusters
    callback_args = {'status_path': ['Status', 'State'], 'sg_list_attribute_name': ['Ec2InstanceAttributes', 'EmrManagedMasterSecurityGroup'], 'sg_id_attribute_name': ''}
    go_to_and_do(aws_config, aws_config['services']['emr'], ['regions', 'vpcs', 'clusters'], ['services', 'emr'], match_security_groups_and_resources_callback, callback_args)
    callback_args = {'status_path': ['Status', 'State'], 'sg_list_attribute_name': ['Ec2InstanceAttributes', 'EmrManagedSlaveSecurityGroup'], 'sg_id_attribute_name': ''}
    go_to_and_do(aws_config, aws_config['services']['emr'], ['regions', 'vpcs', 'clusters'], ['services', 'emr'], match_security_groups_and_resources_callback, callback_args)




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
    if 'status_path' in callback_args:
        status_path = combine_paths(copy.deepcopy(original_resource_path), callback_args['status_path'])
        resource_status = get_object_at(aws_config, status_path)
    else:
        resource_status = None
    unknown_vpc_id = True if current_path[4] != 'vpcs' else False
    # Issue 89 & 91 : can instances have no security group?
    try:
        try:
            sg_attribute = get_object_at(resource, callback_args['sg_list_attribute_name'])
        except:
            return
        if type(sg_attribute) != list:
            sg_attribute = [ sg_attribute ]
        for resource_sg in sg_attribute:
            if type(resource_sg) == dict:
                sg_id = resource_sg[callback_args['sg_id_attribute_name']]
            else:
                sg_id = resource_sg
            if unknown_vpc_id:
                vpc_id = sg_map[sg_id]['vpc_id']
                sg_base_path = copy.deepcopy(current_path[0:4])
                sg_base_path[1] = 'ec2'
                sg_base_path = sg_base_path + [ 'vpcs', vpc_id, 'security_groups' ]
            else:
                sg_base_path = copy.deepcopy(current_path[0:6])
                sg_base_path[1] = 'ec2'
                sg_base_path.append('security_groups')
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


def set_emr_vpc_ids(aws_config):
    clear_list = []
    go_to_and_do(aws_config, aws_config['services']['emr'], ['regions', 'vpcs'], ['services', 'emr'], set_emr_vpc_ids_callback, {'clear_list': clear_list})
    for region in clear_list:
        aws_config['services']['emr']['regions'][region]['vpcs'].pop('TODO')


def set_emr_vpc_ids_callback(aws_config, current_config, path, current_path, vpc_id, callback_args):
    if vpc_id != 'TODO':
        return
    region = current_path[3]
    vpc_id = sg_id = subnet_id = None
    pop_list = []
    for cluster_id in current_config['clusters']:
        cluster = current_config['clusters'][cluster_id]
        if 'EmrManagedMasterSecurityGroup' in cluster['Ec2InstanceAttributes']:
            sg_id = cluster['Ec2InstanceAttributes']['EmrManagedMasterSecurityGroup']
        elif 'RequestedEc2SubnetIds' in cluster['Ec2InstanceAttributes']:
            subnet_id = cluster['Ec2InstanceAttributes']['RequestedEc2SubnetIds']
        else:
            printError('Unable to determine VPC id for EMR cluster %s' % str(cluster_id))
            continue
        if sg_id in sg_map:
            vpc_id = sg_map[sg_id]['vpc_id']
            pop_list.append(cluster_id)
        else:
            sid_found = False
            if subnet_id:
                for sid in subnet_id:
                    if sid in subnet_map:
                        vpc_id = subnet_map[sid]['vpc_id']
                        pop_list.append(cluster_id)
                        sid_found = True
            if not sid_found:
                printError('Unable to determine VPC id for %s' % (str(subnet_id) if subnet_id else str(sg_id)))
                continue
        if vpc_id:
            region_vpcs_config = get_object_at(aws_config, current_path)
            manage_dictionary(region_vpcs_config, vpc_id, {'clusters': {}})
            region_vpcs_config[vpc_id]['clusters'][cluster_id] = cluster
    for cluster_id in pop_list:
        current_config['clusters'].pop(cluster_id)
    if len(current_config['clusters']) == 0:
        callback_args['clear_list'].append(region)


def parse_elb_policies(aws_config):
    """
    TODO

    :param aws_config:
    :return:
    """
    if 'elb' in aws_config['services']:
        go_to_and_do(aws_config, aws_config['services']['elb'], ['regions'], [], parse_elb_policies_callback, {})

    #if 'elbv2' in aws_config['services']:
        # Do something too here...


def parse_elb_policies_callback(aws_config, current_config, path, current_path, region_id, callback_args):
    region_config = get_object_at(aws_config, [ 'services', 'elb', ] + current_path + [ region_id ])
    region_config['elb_policies'] = current_config['elb_policies']
    for policy_id in region_config['elb_policies']:
        if region_config['elb_policies'][policy_id]['PolicyTypeName'] != 'SSLNegotiationPolicyType':
            continue
        # protocols, options, ciphers
        policy = region_config['elb_policies'][policy_id]
        protocols = {}
        options = {}
        ciphers = {}
        for attribute in policy['PolicyAttributeDescriptions']:
            if attribute['AttributeName'] in [ 'Protocol-SSLv3', 'Protocol-TLSv1', 'Protocol-TLSv1.1', 'Protocol-TLSv1.2' ]:
                protocols[attribute['AttributeName']] = attribute['AttributeValue']
            elif attribute['AttributeName'] in [ 'Server-Defined-Cipher-Order' ]:
                options[attribute['AttributeName']] = attribute['AttributeValue']
            elif attribute['AttributeName'] == 'Reference-Security-Policy':
                policy['reference_security_policy'] = attribute['AttributeValue']
            else:
                ciphers[attribute['AttributeName']] = attribute['AttributeValue']
            policy['protocols'] = protocols
            policy['options'] = options
            policy['ciphers'] = ciphers
            # TODO: pop ?


def sort_vpc_flow_logs(vpc_config):
    go_to_and_do(vpc_config, None, ['regions', 'flow_logs'], [], sort_vpc_flow_logs_callback, {})


def sort_vpc_flow_logs_callback(vpc_config, current_config, path, current_path, flow_log_id, callback_args):
    attached_resource = current_config['ResourceId']
    if attached_resource.startswith('vpc-'):
        vpc_path = combine_paths(current_path[0:2], ['vpcs', attached_resource])
        try:
            attached_vpc = get_object_at(vpc_config, vpc_path)
        except Exception as e:
            printDebug('It appears that the flow log %s is attached to a resource that was previously deleted (%s).' % (flow_log_id, attached_resource))
            return
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
        if i:
            printInfo('Index: %s' % str(i))
        printInfo('Path: %s' % str(current_path))
        printInfo('Key = %s' % str(key))
        printInfo('Value = %s' % str(value))
        printInfo('Path = %s' % path)
