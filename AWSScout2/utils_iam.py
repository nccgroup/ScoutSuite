
# Import opinel
from opinel.utils_iam import *

# Import Scout2 tools
from AWSScout2.utils import *
from AWSScout2.filters import *
from AWSScout2.findings import *

# Import third-party packages
import base64
import json
import urllib


########################################
##### IAM functions
########################################

def analyze_iam_config(iam_info, force_write):
    sys.stdout.write('Analyzing IAM data...\n')
    analyze_config(iam_finding_dictionary, iam_filter_dictionary, iam_info, 'IAM', force_write)

def get_groups_info(iam_client, iam_info):
    groups = handle_truncated_response(iam_client.list_groups, {}, ['Groups'])
    iam_info['GroupsCount'] = len(groups)
    thread_work(iam_client, iam_info, groups['Groups'], get_group_info, num_threads = 10)
    show_status(iam_info, 'Groups')

def get_group_info(iam_client, q, params):
    while True:
        try:
            iam_info, group = q.get()
            # When resuming upon throttling error, skip if already fetched
            if group['GroupName'] in iam_info['Groups']:
                continue
            group['Id'] = group.pop('GroupId')
            group['Name'] = group.pop('GroupName')
            group['Users'] = get_group_users(iam_client, group['Name']);
            group['Policies'] = get_inline_policies(iam_client, iam_info, 'group', group['Name'])
            iam_info['Groups'][group['Name']] = group
            show_status(iam_info, 'Groups', False)
        except Exception, e:
            printException(e)
            pass
        finally:
            q.task_done()

def get_group_users(iam_client, group_name):
    users = []
    fetched_users = iam_client.get_group(GroupName = group_name)['Users']
    for user in fetched_users:
        users.append(user['UserName'])
    return users

def get_iam_info(key_id, secret, session_token, iam_info):
    manage_dictionary(iam_info, 'Groups', {})
    manage_dictionary(iam_info, 'Permissions', {})
    manage_dictionary(iam_info, 'Roles', {})
    manage_dictionary(iam_info, 'Users', {})
    iam_client = connect_iam(key_id, secret, session_token)
    # Generate the report early so that download doesn't fail with "ReportInProgress".
    try:
        iam_client.generate_credential_report()
    except Exception, e:
        pass
    print 'Fetching IAM users...'
    get_users_info(iam_client, iam_info)
    print 'Fetching IAM groups...'
    get_groups_info(iam_client, iam_info)
    print 'Fetching IAM roles...'
    get_roles_info(iam_client, iam_info)
    print 'Fetching IAM policies...'
    get_managed_policies(iam_client, iam_info)
    print 'Fetching IAM credential report...'
    get_credential_report(iam_client, iam_info)

def get_permissions(policy_document, permissions, keyword, name, policy_name, is_managed_policy = False):
    manage_dictionary(permissions, 'Action', {})
    manage_dictionary(permissions, 'NotAction', {})
    if type(policy_document['Statement']) != list:
        parse_statement(policy_document, permissions, keyword, name, policy_name, is_managed_policy, policy_document['Statement'])
    else:
        for statement in policy_document['Statement']:
            parse_statement(policy_document, permissions, keyword, name, policy_name, is_managed_policy, statement)

def parse_statement(policy_document, permissions, keyword, name, policy_name, is_managed_policy, statement):
        effect = str(statement['Effect'])
        action_string = 'Action' if 'Action' in statement else 'NotAction'
        resource_string = 'Resource' if 'Resource' in statement else 'NotResource'
        condition = statement['Condition'] if 'Condition' in statement else None
        parse_actions(permissions[action_string], statement[action_string], resource_string, statement[resource_string], effect, keyword, name, policy_name, is_managed_policy, condition)

def parse_actions(permissions, actions, resource_string, resources, effect, keyword, name, policy_name, is_managed_policy, condition):
    if type(actions) == list:
        for action in actions:
            parse_action(permissions, action, resource_string, resources, effect, keyword, name, policy_name, is_managed_policy, condition)
    else:
        parse_action(permissions, actions, resource_string, resources, effect, keyword, name, policy_name, is_managed_policy, condition)

def parse_action(permissions, action, resource_string, resources, effect, keyword, name, policy_name, is_managed_policy, condition):
    manage_dictionary(permissions, action, {})
    parse_resources(permissions[action], resource_string, resources, effect, keyword, name, policy_name, is_managed_policy, condition)

def parse_resources(permission, resource_string, resources, effect, keyword, name, policy_name, is_managed_policy, condition):
    if type(resources) == list:
        for resource in resources:
            parse_resource(permission, resource_string, resource, effect, keyword, name, policy_name, is_managed_policy, condition)
    else:
        parse_resource(permission, resource_string, resources, effect, keyword, name, policy_name, is_managed_policy, condition)

def parse_resource(permission, resource_string, resource, effect, keyword, name, policy_name, is_managed_policy, condition):
    manage_dictionary(permission, keyword, {})
    manage_dictionary(permission[keyword], effect, {})
    manage_dictionary(permission[keyword][effect], name, {})
    manage_dictionary(permission[keyword][effect][name], resource_string, {})
    manage_dictionary(permission[keyword][effect][name][resource_string], resource, {})
    if is_managed_policy:
        policy_type = 'ManagedPolicies'
    else:
        policy_type = 'InlinePolicies'
    manage_dictionary(permission[keyword][effect][name][resource_string][resource], policy_type, {})
    manage_dictionary(permission[keyword][effect][name][resource_string][resource][policy_type], policy_name, {})
    permission[keyword][effect][name][resource_string][resource][policy_type][policy_name]['condition'] = condition

def handle_truncated_response(iam_method, params, entities):
    results = {}
    for entity in entities:
        results[entity] = []
    while True:
        response = iam_method(**params)
        for entity in entities:
            results[entity] = results[entity] + response[entity]
        if 'IsTruncated' in response and response['IsTruncated'] == True:
            params['Marker'] = response['Marker']
        else:
            break
    return results

def get_managed_policies(iam_client, iam_info):
    policies = []
    params = {}
    params['OnlyAttached'] = True
    policies = handle_truncated_response(iam_client.list_policies, params, ['Policies'])
    manage_dictionary(iam_info, 'ManagedPolicies', {})
    iam_info['ManagedPoliciesCount'] = len(policies['Policies'])
    show_status(iam_info, 'ManagedPolicies', False)
    thread_work(iam_client, iam_info, policies['Policies'], get_managed_policy, num_threads = 10)
    show_status(iam_info, 'ManagedPolicies')

def get_managed_policy(iam_client, q, params):
    while True:
        try:
            iam_info, policy = q.get()
            manage_dictionary(iam_info['ManagedPolicies'], policy['Arn'], {})
            iam_info['ManagedPolicies'][policy['Arn']]['PolicyName'] = policy['PolicyName']
            iam_info['ManagedPolicies'][policy['Arn']]['PolicyId'] = policy['PolicyId']
            # Download version and document
            policy_version = iam_client.get_policy_version(PolicyArn = policy['Arn'], VersionId = policy['DefaultVersionId'])
            policy_version = policy_version['PolicyVersion']
            iam_info['ManagedPolicies'][policy['Arn']]['PolicyDocument'] = policy_version['Document']
            # Get attached IAM entities
            attached_entities = handle_truncated_response(iam_client.list_entities_for_policy, {'PolicyArn': policy['Arn']}, ['PolicyGroups', 'PolicyRoles', 'PolicyUsers'])
            for entity_type in attached_entities:
                type_field = entity_type.replace('Policy', '').title()
                for entity in attached_entities[entity_type]:
                    name_field = entity_type.replace('Policy', '')[:-1] + 'Name'
                    manage_dictionary(iam_info[type_field][entity[name_field]], 'ManagedPolicies', [])
                    iam_info[type_field][entity[name_field]]['ManagedPolicies'].append(policy['Arn'])
                    get_permissions(policy_version['Document'], iam_info['Permissions'], type_field, entity[name_field], policy['Arn'], True)
            show_status(iam_info, 'ManagedPolicies', False)
        except Exception, e:
            printException(e)
            pass
        finally:
            q.task_done()

def get_inline_policies(iam_client, iam_info, keyword, name):
    fetched_policies = {}
    get_policy_method = getattr(iam_client, 'get_' + keyword + '_policy')
    list_policy_method = getattr(iam_client, 'list_' + keyword + '_policies')
    args = {}
    args[keyword.title() + 'Name'] = name
    try:
        policy_names = list_policy_method(**args)['PolicyNames']
    except Exception as e:
        printException(e)
        return fetched_policies
    try:
        for policy_name in policy_names:
            args['PolicyName'] = policy_name
            policy_document = get_policy_method(**args)['PolicyDocument']
            manage_dictionary(fetched_policies, policy_name, {})
            fetched_policies[policy_name]['PolicyDocument'] = policy_document
            get_permissions(policy_document, iam_info['Permissions'], keyword + 's', name, policy_name)
    except Exception as e:
        printException(e)
    return fetched_policies

def get_roles_info(iam_client, iam_info):
    roles = handle_truncated_response(iam_client.list_roles, {}, ['Roles'])
    iam_info['RolesCount'] = len(roles)
    thread_work(iam_client, iam_info, roles['Roles'], get_role_info, num_threads = 10)
    show_status(iam_info, 'Roles')

def get_role_info(iam_client, q, params):
    while True:
        try:
            iam_info, role = q.get()
            # When resuming upon throttling error, skip if already fetched
            if role['RoleName'] in iam_info['Roles']:
                continue
            role['Id'] = role.pop('RoleId')
            role['Name'] = role.pop('RoleName')
            role['Policies'] = get_inline_policies(iam_client, iam_info, 'role', role['Name'])
            profiles = handle_truncated_response(iam_client.list_instance_profiles_for_role, {'RoleName': role['Name']}, ['InstanceProfiles'])
            manage_dictionary(role, 'InstanceProfiles', {})
            for profile in profiles['InstanceProfiles']:
                manage_dictionary(role['InstanceProfiles'], profile['Arn'], {})
                role['InstanceProfiles'][profile['Arn']]['Id'] = profile['InstanceProfileId']
                role['InstanceProfiles'][profile['Arn']]['Name'] = profile['InstanceProfileName']
            iam_info['Roles'][role['Name']] = role
            show_status(iam_info, 'Roles', False)
        except Exception, e:
            printException(e)
            pass
        finally:
            q.task_done()

def get_credential_report(iam_client, iam_info):
    iam_report = {}
    try:
        report = iam_client.get_credential_report()['Content']
        lines = report.split('\n')
        keys = lines[0].split(',')
        for line in lines[1:]:
            values = line.split(',')
            manage_dictionary(iam_report, values[0], {})
            for key, value in zip(keys, values):
                iam_report[values[0]][key] = value
        iam_info['CredentialReport'] = iam_report
    except Exception, e:
        print 'Failed to generate/download a credential report.'
        print e

def get_users_info(iam_client, iam_info):
    users = handle_truncated_response(iam_client.list_users, {}, ['Users'])
    iam_info['UsersCount'] = len(users['Users'])
    thread_work(iam_client, iam_info, users['Users'], get_user_info, num_threads = 10)
    show_status(iam_info, 'Users')

def get_user_info(iam_client, q, params):
    while True:
        try:
            iam_info, user = q.get()
            # When resuming upon throttling error, skip if already fetched
            if user['UserName'] in iam_info['Users']:
                continue
            user['Id'] = user.pop('UserId')
            user['Name'] = user.pop('UserName')
            user['Policies'] = get_inline_policies(iam_client, iam_info, 'user', user['Name'])
            user['Groups'] = handle_truncated_response(iam_client.list_groups_for_user, {'UserName': user['Name']}, ['Groups'])['Groups']
            try:
                user['LoginProfile'] = iam_client.get_login_profiles(UserName = user['Name'])['LoginProfile']
            except Exception, e:
                pass
            user['AccessKeys'] = iam_client.list_access_keys(UserName = user['Name'])['AccessKeyMetadata']
            user['MFADevices'] = iam_client.list_mfa_devices(UserName = user['Name'])['MFADevices']
            iam_info['Users'][user['Name']] = user
            show_status(iam_info, 'Users', False)
        except Exception, e:
            printException(e)
            pass
        finally:
            q.task_done()

def show_status(iam_info, entities, newline = True):
    current = len(iam_info[entities])
    total = iam_info[entities + 'Count']
    sys.stdout.write("\r%d/%d" % (current, total))
    sys.stdout.flush()
    if newline:
        sys.stdout.write('\n')
