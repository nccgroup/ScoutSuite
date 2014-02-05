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
    print 'Analyzing IAM data...'
    iam_config = {"groups": groups, "permissions": permissions, "roles": roles, "users": users['list_users_response']['list_users_result']['users']}
    for finding in iam_finding_dictionary['violations']:
        for entity in iam_config[finding.entity]:
            finding.callback(finding, entity)
    save_json_to_file(iam_finding_dictionary.to_JSON(), 'IAM violations', True)

def get_groups_info(iam, permissions):
    groups = iam.get_all_groups()
    for group in groups.list_groups_response.list_groups_result.groups:
        group['users'] = get_group_users(iam, group.group_name);
        group['policies'], permissions = get_policies(iam, permissions, 'group', group.group_name)
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
    roles = iam.list_roles()
    for role in roles.list_roles_response.list_roles_result.roles:
        role['policies'], permissions = get_policies(iam, permissions, 'role', role.role_name)
    return roles, permissions

def get_users_info(iam, permissions):
    users = iam.get_all_users()
    for user in users.list_users_response.list_users_result.users:
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

    return users, permissions
