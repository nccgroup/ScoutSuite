# -*- coding: utf-8 -*-
"""
Multi-service post-processing functions
"""

from opinel.utils import manage_dictionary, printInfo, printError, printException

def do_postprocessing(aws_config):
    match_instances_and_roles(aws_config)
    match_iam_policies_and_buckets(aws_config)
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
        if 'managed_policies' in policy_info:
            manage_dictionary(bucket[iam_entity][allowed_iam_entity], 'managed_policies', {})
            bucket[iam_entity][allowed_iam_entity]['managed_policies'].update(policy_info['managed_policies'])
    elif bucket_name == '*':
        for bucket in s3_info['buckets']:
            __update_iam_permissions(s3_info, bucket, iam_entity, allowed_iam_entity, policy_info)
        pass
    else:
        # Could be an error or cross-account access, ignore...
        pass
