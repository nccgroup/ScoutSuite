# Import opinel
from opinel.utils_iam import *

# Import Scout2 tools
from AWSScout2.utils import *
from AWSScout2.filters import *
from AWSScout2.findings import *

# Import stock packages
import base64
import json
import urllib

########################################
##### IAM functions
########################################

def analyze_iam_config(iam_info, aws_account_id, force_write):
    printInfo('Analyzing IAM data...')
    analyze_config(iam_finding_dictionary, iam_filter_dictionary, iam_info, 'IAM', force_write)

def get_account_password_policy(iam_client, iam_info):
    iam_info['password_policy'] = iam_client.get_account_password_policy()['PasswordPolicy']
    if 'PasswordReusePrevention' not in iam_info['password_policy']:
        iam_info['password_policy']['PasswordReusePrevention'] = False
    else:
        iam_info['password_policy']['PreviousPasswordPrevented'] = iam_info['password_policy']['PasswordReusePrevention']
        iam_info['password_policy']['PasswordReusePrevention'] = True
    # There is a bug in the API: ExpirePasswords always returns false
    if 'MaxPasswordAge' in iam_info['password_policy']:
        iam_info['password_policy']['ExpirePasswords'] = True

def get_aws_account_id(iam_info):
    for resources in ['groups', 'roles', 'users']:
        if resources in iam_info:
            for resource in iam_info[resources]:
                try:
                    return iam_info[resources][resource]['Arn'].split(':')[4]
                except:
                    pass

def get_groups_info(iam_client, iam_info):
    groups = handle_truncated_response(iam_client.list_groups, {}, 'Marker', ['Groups'])
    iam_info['groups_count'] = len(groups['Groups'])
    thread_work(groups['Groups'], get_group_info, params = {'iam_client': iam_client, 'iam_info': iam_info}, num_threads = 10)
    show_status(iam_info, 'groups')

def get_group_info(q, params):
    iam_client = params['iam_client']
    iam_info = params['iam_info']
    while True:
        try:
            group = q.get()
            # When resuming upon throttling error, skip if already fetched
            if group['GroupName'] in iam_info['groups']:
                continue
            group['id'] = group.pop('GroupId')
            group['name'] = group.pop('GroupName')
            group['users'] = get_group_users(iam_client, group['name']);
            policies = get_inline_policies(iam_client, iam_info, 'group', group['name'])
            if len(policies):
                group['inline_policies'] = policies
            iam_info['groups'][group['id']] = group
            show_status(iam_info, 'groups', False)
        except Exception as e:
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

def get_iam_info(key_id, secret, session_token, service_config):
    manage_dictionary(service_config, 'groups', {})
    manage_dictionary(service_config, 'permissions', {})
    manage_dictionary(service_config, 'roles', {})
    manage_dictionary(service_config, 'users', {})
    iam_client = connect_iam(key_id, secret, session_token)
    # Generate the report early so that download doesn't fail with "ReportInProgress".
    try:
        iam_client.generate_credential_report()
    except Exception as e:
        pass
    printInfo('Fetching IAM users...')
    get_users_info(iam_client, service_config)
    printInfo('Fetching IAM groups...')
    get_groups_info(iam_client, service_config)
    printInfo('Fetching IAM roles...')
    get_roles_info(iam_client, service_config)
    printInfo('Fetching IAM policies...')
    get_managed_policies(iam_client, service_config)
    printInfo('Fetching IAM credential report...')
    get_credential_report(iam_client, service_config)
    printInfo('Fetching IAM password policy...')
    get_account_password_policy(iam_client, service_config)

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
    keyword = keyword.title()
    manage_dictionary(permission, keyword, {})
    manage_dictionary(permission[keyword], effect, {})
    manage_dictionary(permission[keyword][effect], name, {})
    manage_dictionary(permission[keyword][effect][name], resource_string, {})
    manage_dictionary(permission[keyword][effect][name][resource_string], resource, {})
    if is_managed_policy:
        policy_type = 'managed_policies'
    else:
        policy_type = 'inline_policies'
    manage_dictionary(permission[keyword][effect][name][resource_string][resource], policy_type, {})
    manage_dictionary(permission[keyword][effect][name][resource_string][resource][policy_type], policy_name, {})
    permission[keyword][effect][name][resource_string][resource][policy_type][policy_name]['condition'] = condition

def get_managed_policies(iam_client, iam_info):
    policies = []
    params = {}
    params['OnlyAttached'] = True
    policies = handle_truncated_response(iam_client.list_policies, params, 'Marker', ['Policies'])
    manage_dictionary(iam_info, 'managed_policies', {})
    iam_info['managed_policies_count'] = len(policies['Policies'])
    show_status(iam_info, 'managed_policies', False)
    thread_work(policies['Policies'], get_managed_policy, params = {'iam_client': iam_client, 'iam_info': iam_info}, num_threads = 10)
    show_status(iam_info, 'managed_policies')

def get_managed_policy(q, params):
    iam_client = params['iam_client']
    iam_info = params['iam_info']
    while True:
        try:
            policy = q.get()
            manage_dictionary(iam_info['managed_policies'], policy['Arn'], {})
            iam_info['managed_policies'][policy['Arn']]['name'] = policy['PolicyName']
            iam_info['managed_policies'][policy['Arn']]['id'] = policy['PolicyId']
            # Download version and document
            policy_version = iam_client.get_policy_version(PolicyArn = policy['Arn'], VersionId = policy['DefaultVersionId'])
            policy_version = policy_version['PolicyVersion']
            iam_info['managed_policies'][policy['Arn']]['PolicyDocument'] = policy_version['Document']
            # Get attached IAM entities
            attached_entities = handle_truncated_response(iam_client.list_entities_for_policy, {'PolicyArn': policy['Arn']}, 'Marker', ['PolicyGroups', 'PolicyRoles', 'PolicyUsers'])
            for entity_type in attached_entities:
                resource_type = entity_type.replace('Policy', '').lower()
                for entity in attached_entities[entity_type]:
                    name_field = entity_type.replace('Policy', '')[:-1] + 'Name'
                    resource_name = entity[name_field]
                    resource_id = get_id_for_resource(iam_info, resource_type, resource_name)
                    manage_dictionary(iam_info[resource_type][resource_id], 'managed_policies', [])
                    iam_info[resource_type][resource_id]['managed_policies'].append(policy['Arn'])
                    get_permissions(policy_version['Document'], iam_info['permissions'], resource_type, resource_id, policy['Arn'], True)
            show_status(iam_info, 'managed_policies', False)
        except Exception as e:
            printException(e)
            pass
        finally:
            q.task_done()

def get_id_for_resource(iam_info, resource_type, resource_name):
    for resource_id in iam_info[resource_type]:
        if iam_info[resource_type][resource_id]['name'] == resource_name:
            return resource_id


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
            get_permissions(policy_document, iam_info['permissions'], keyword + 's', name, policy_name)
    except Exception as e:
        printException(e)
    return fetched_policies

def get_roles_info(iam_client, iam_info):
    roles = handle_truncated_response(iam_client.list_roles, {}, 'Marker', ['Roles'])
    iam_info['roles_count'] = len(roles['Roles'])
    thread_work(roles['Roles'], get_role_info, params = {'iam_client': iam_client, 'iam_info': iam_info}, num_threads = 10)
    show_status(iam_info, 'roles')

def get_role_info(q, params):
    iam_client = params['iam_client']
    iam_info = params['iam_info']
    while True:
        try:
            role = q.get()
            # When resuming upon throttling error, skip if already fetched
            if role['RoleName'] in iam_info['roles']:
                continue
            role['id'] = role.pop('RoleId')
            role['name'] = role.pop('RoleName')
            policies = get_inline_policies(iam_client, iam_info, 'role', role['name'])
            if len(policies):
                role['inline_policies'] = policies
            profiles = handle_truncated_response(iam_client.list_instance_profiles_for_role, {'RoleName': role['name']}, 'Marker', ['InstanceProfiles'])
            manage_dictionary(role, 'InstanceProfiles', {})
            for profile in profiles['InstanceProfiles']:
                manage_dictionary(role['InstanceProfiles'], profile['Arn'], {})
                role['InstanceProfiles'][profile['Arn']]['id'] = profile['InstanceProfileId']
                role['InstanceProfiles'][profile['Arn']]['name'] = profile['InstanceProfileName']
            iam_info['roles'][role['id']] = role
            show_status(iam_info, 'roles', False)
        except Exception as e:
            printException(e)
            pass
        finally:
            q.task_done()

def get_credential_report(iam_client, iam_info):
    iam_report = {}
    try:
        report = iam_client.get_credential_report()['Content']
        lines = report.splitlines()
        keys = lines[0].decode('utf-8').split(',')
        for line in lines[1:]:
            values = line.decode('utf-8').split(',')
            manage_dictionary(iam_report, values[0], {})
            for key, value in zip(keys, values):
                iam_report[values[0]][key] = value
        iam_info['credential_report'] = iam_report
    except Exception as e:
        printError('Failed to generate/download a credential report.')
        printException(e)

def get_users_info(iam_client, iam_info):
    users = handle_truncated_response(iam_client.list_users, {}, 'Marker', ['Users'])
    iam_info['users_count'] = len(users['Users'])
    thread_work(users['Users'], get_user_info, params = {'iam_client': iam_client, 'iam_info': iam_info}, num_threads = 10)
    show_status(iam_info, 'users')

def get_user_info(q, params):
    iam_client = params['iam_client']
    iam_info = params['iam_info']
    while True:
        try:
            user = q.get()
            # When resuming upon throttling error, skip if already fetched
            if user['UserName'] in iam_info['users']:
                continue
            user['id'] = user.pop('UserId')
            user['name'] = user.pop('UserName')
            policies = get_inline_policies(iam_client, iam_info, 'user', user['name'])
            if len(policies):
                user['inline_policies'] = policies
            user['groups'] = []
            groups = handle_truncated_response(iam_client.list_groups_for_user, {'UserName': user['name']}, 'Marker', ['Groups'])['Groups']
            for group in groups:
                user['groups'].append(group['GroupName'])
            try:
                user['LoginProfile'] = iam_client.get_login_profile(UserName = user['name'])['LoginProfile']
            except Exception as e:
                pass
            user['AccessKeys'] = iam_client.list_access_keys(UserName = user['name'])['AccessKeyMetadata']
            user['MFADevices'] = iam_client.list_mfa_devices(UserName = user['name'])['MFADevices']
            iam_info['users'][user['id']] = user
            show_status(iam_info, 'users', False)
        except Exception as e:
            printException(e)
            pass
        finally:
            q.task_done()

def show_status(iam_info, entities, newline = True):
    current = len(iam_info[entities])
    total = iam_info[entities + '_count']
    sys.stdout.write("\r%d/%d" % (current, total))
    sys.stdout.flush()
    if newline:
        sys.stdout.write('\n')
