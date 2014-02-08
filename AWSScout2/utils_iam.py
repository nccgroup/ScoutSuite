#!/usr/bin/env python

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.findings_iam import *

# Import other third-party packages
import json
import urllib


########################################
##### IAM functions
########################################

def analyze_iam_config(groups, permissions, roles, users):
    sys.stdout.write('Analyzing IAM data...\n')
    iam_config = {"groups": groups, "permissions": permissions, "roles": roles, "users": users}
    analyze_config(iam_finding_dictionary, iam_config, 'IAM violations')

def get_groups_info(iam, permissions):
    groups = handle_truncated_responses(iam.get_all_groups, ['list_groups_response', 'list_groups_result'], 'groups')
    count, total = init_status(groups)
    for group in groups:
        count = update_status(count, total)
        group['users'] = get_group_users(iam, group.group_name);
        group['policies'], permissions = get_policies(iam, permissions, 'group', group.group_name)
    close_status()
    return groups, permissions

def get_group_users(iam, group_name):
    users = []
    fetched_users = iam.get_group(group_name).get_group_response.get_group_result.users
    for user in fetched_users:
        users.append(user.user_name)
    return users

def get_permissions(policy_document, permissions, keyword, name, policy_name):
    document = json.loads(urllib.unquote(policy_document).decode('utf-8'))
    for statement in document['Statement']:
        if 'Effect' and 'Action' in statement:
            effect = str(statement['Effect'])
            for action in statement['Action']:
                permissions = manage_dictionary(permissions, action, {})
                permissions[action] = manage_dictionary(permissions[action], effect, {})
                permissions[action][effect] = manage_dictionary(permissions[action][effect], keyword, [])
                entry = {}
                entry['name'] = name
                entry['policy_name'] = policy_name
                permissions[action][effect][keyword].append(entry)
    return permissions

def get_policies(iam, permissions, keyword, name):
    fetched_policies = []
    if keyword == 'role':
        m1 = getattr(iam, 'list_role_policies', None)
    else:
        m1 = getattr(iam, 'get_all_' + keyword + '_policies', None)
    if m1:
        policy_names = m1(name)
    else:
        return fetched_policies, permissions
    policy_names = policy_names['list_' + keyword + '_policies_response']['list_' + keyword + '_policies_result']['policy_names']
    get_policy_method = getattr(iam, 'get_' + keyword + '_policy')
    for policy_name in policy_names:
        r = get_policy_method(name, policy_name)
        r = r['get_'+keyword+'_policy_response']['get_'+keyword+'_policy_result']
        pdetails = {}
        pdetails['policy_name'] = policy_name
        pdetails['policy_document'] = r.policy_document
        fetched_policies.append(pdetails)
        permissions = get_permissions(pdetails['policy_document'], permissions, keyword + 's', name, pdetails['policy_name'])
    return fetched_policies, permissions


def get_roles_info(iam, permissions):
    roles = handle_truncated_responses(iam.list_roles, ['list_roles_response', 'list_roles_result'], 'roles')
    count, total = init_status(roles)
    for role in roles:
        count = update_status(count, total)
        role['policies'], permissions = get_policies(iam, permissions, 'role', role.role_name)
    close_status()
    return roles, permissions

def get_users_info(iam, permissions):
    users = handle_truncated_responses(iam.get_all_users, ['list_users_response', 'list_users_result'], 'users')
    count, total = init_status(users)
    for user in users:
        count = update_status(count, total)
        user['policies'], permissions = get_policies(iam, permissions, 'user', user.user_name)
        groups = iam.get_groups_for_user(user['user_name'])
        user['groups'] = groups.list_groups_for_user_response.list_groups_for_user_result.groups
        try:
            logins = iam.get_login_profiles(user['user_name'])
            user['logins'] = logins.get_login_profile_response.get_login_profile_result.login_profile
        except Exception, e:
            pass
        access_keys = iam.get_all_access_keys(user['user_name'])
        user['access_keys'] = access_keys.list_access_keys_response.list_access_keys_result.access_key_metadata
        mfa_devices = iam.get_all_mfa_devices(user['user_name'])
        user['mfa_devices'] = mfa_devices.list_mfa_devices_response.list_mfa_devices_result.mfa_devices
    close_status()
    return users, permissions

def handle_truncated_responses(callback, result_path, items_name):
    marker_value = None
    items = []
    while True:
        result = callback(marker = marker_value)
        for key in result_path:
            result = result[key]
        marker_value = result['marker'] if result['is_truncated'] != 'false' else None
        items = items + result[items_name]
        if marker_value is None:
            break
    sys.stdout.write('Received %s %s, fetching data... (this may take a while)\n' % (str(len(items)), items_name))
    return items
