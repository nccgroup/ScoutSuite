# -*- coding: utf-8 -*-
"""
IAM-related classes and functions
"""

# Import opinel
#from opinel.utils_iam import *

# Import Scout2 tools
from AWSScout2.BaseConfig import BaseConfig
from AWSScout2.utils import *

# Import stock packages
import base64
import json
import urllib

class IAMConfig(BaseConfig):
    """
    Object that holds the IAM configuration

    :ivar credential_report:    Credential report as downloaded from the AWS API
    :ivar groups:               Dictionary of IAM groups in the AWS account
    :ivar groups_count:         len(groups)
    :ivar password_policy:      Account password policy
    :ivar permissions:          Summary of permissions granted via all IAM policies
    :ivar policies:             Dictionary of IAM managed policies in use within the AWS Account
    :ivar policies_count:       len(policies)
    :ivar roles:                Dictionary of IAM roles in the AWS account
    :ivar roles_count:          len(roles)
    :ivar users:                Dictionary of IAM users in the AWS account
    :ivar users_count:          len(users)
    """

    targets = (
        ('groups', 'Groups', 'list_groups', {}, False),
        ('policies', 'Policies', 'list_policies', {'OnlyAttached': True}, False),
        ('roles', 'Roles', 'list_roles', {}, False),
        ('users', 'Users', 'list_users', {}, False),
    )

    def __init__(self):
        self.credential_report = {}
        self.groups = {}
        self.groups_count = 0
        self.password_policy = {}
        self.permissions = {}
        self.policies = {}
        self.policies_count = 0
        self.roles = {}
        self.roles_count = 0
        self.users = {}
        self.users_count = 0
        super(IAMConfig, self).__init__()



    ########################################
    ##### Credential report
    ########################################
    def fetch_credential_report(self, api_client, ignore_exception = False):
        """
        Fetch the credential report

        :param: api_client
        :type: FOO
        :param: ignore_exception : initiate credential report creation as not  always ready
        :type: Boolean
        """
        iam_report = {}
        try:
            report = api_client.get_credential_report()['Content']
            lines = report.splitlines()
            keys = lines[0].decode('utf-8').split(',')
            for line in lines[1:]:
                values = line.decode('utf-8').split(',')
                manage_dictionary(iam_report, values[0], {})
                for key, value in zip(keys, values):
                    iam_report[values[0]][key] = value
            self.credential_report = iam_report
            if not ignore_exception:
                printInfo(' Credential report: 1/1')
        except Exception as e:
            if ignore_exception:
                pass
            printError('Failed to generate/download a credential report.')
            printException(e)


    def parse_groups(self, group, params):
        """
        Parse a single IAM group and fetch additional information
        """
        # When resuming upon throttling error, skip if already fetched
        api_client = params['api_client']
        if group['GroupName'] in self.groups:
            return
        api_client = params['api_client']
        # Ensure consistent attribute names across resource types
        group['id'] = group.pop('GroupId')
        group['name'] = group.pop('GroupName')
        group['arn'] = group.pop('Arn')
        # Get group's members
        group['users'] = self.__fetch_group_users(api_client, group['name']);
        # Get inline policies
        policies = self.__get_inline_policies(api_client, 'group', group['id'], group['name'])
        if len(policies):
            group['inline_policies'] = policies
        group['inline_policies_count'] = len(policies)
        self.groups[group['id']] = group



    ########################################
    ##### Inline policies
    ########################################
    def __get_inline_policies(self, api_client, resource_type, resource_id, resource_name):
        fetched_policies = {}
        get_policy_method = getattr(api_client, 'get_' + resource_type + '_policy')
        list_policy_method = getattr(api_client, 'list_' + resource_type + '_policies')
        args = {}
        args[resource_type.title() + 'Name'] = resource_name
        try:
            policy_names = list_policy_method(**args)['PolicyNames']
        except Exception as e:
            printException(e)
            return fetched_policies
        try:
            for policy_name in policy_names:
                args['PolicyName'] = policy_name
                policy_document = get_policy_method(**args)['PolicyDocument']
                policy_id = get_non_aws_id(policy_name)
                manage_dictionary(fetched_policies, policy_id, {})
                fetched_policies[policy_id]['PolicyDocument'] = policy_document
                fetched_policies[policy_id]['name'] = policy_name
#                get_permissions(policy_document, iam_info['permissions'], resource_type + 's', resource_id, policy_id)
        except Exception as e:
            printException(e)
        return fetched_policies



    ########################################
    ##### Managed policies
    ########################################
    def parse_policies(self, fetched_policy, params):
        """
        Parse a single IAM policy and fetch additional information
        """
        api_client = params['api_client']
        policy = {}
        policy['name'] = fetched_policy.pop('PolicyName')
        policy['id'] = fetched_policy.pop('PolicyId')
        policy['arn'] = fetched_policy.pop('Arn')
        # Download version and document
        policy_version = api_client.get_policy_version(PolicyArn = policy['arn'], VersionId = fetched_policy['DefaultVersionId'])
        policy_version = policy_version['PolicyVersion']
        policy['PolicyDocument'] = policy_version['Document']
        # Get attached IAM entities
        policy['attached_to'] = {}
        attached_entities = handle_truncated_response(api_client.list_entities_for_policy, {'PolicyArn': policy['arn']}, ['PolicyGroups', 'PolicyRoles', 'PolicyUsers'])
        for entity_type in attached_entities:
            resource_type = entity_type.replace('Policy', '').lower()
            if len(attached_entities[entity_type]):
                policy['attached_to'][resource_type] = []
            for entity in attached_entities[entity_type]:
                name_field = entity_type.replace('Policy', '')[:-1] + 'Name'
                resource_name = entity[name_field]
                resource_id = self.get_id_for_resource(resource_type, resource_name)
#                policy['attached_to'][resource_type].append({'id': resource_id, 'name': resource_name})
#                manage_dictionary(iam_info[resource_type][resource_id], 'managed_policies', [])
#                manage_dictionary(iam_info[resource_type][resource_id], 'managed_policies_count', 0)
#                iam_info[resource_type][resource_id]['managed_policies'].append(policy['id'])
#                iam_info[resource_type][resource_id]['managed_policies_count'] = iam_info[resource_type][resource_id]['managed_policies_count'] + 1
#                get_permissions(policy_version['Document'], iam_info['permissions'], resource_type, resource_id, policy['id'], True)
        # Save policy
        self.policies[policy['id']] = policy



    ########################################
    ##### Password policy
    ########################################
    def fetch_password_policy(self, api_client):
        """
        Fetch the password policy that applies to all IAM users within the AWS account
        """
        try:
            self.password_policy = api_client.get_account_password_policy()['PasswordPolicy']
            if 'PasswordReusePrevention' not in self.password_policy:
                self.password_policy['PasswordReusePrevention'] = False
            else:
                self.password_policy['PreviousPasswordPrevented'] = self.password_policy['PasswordReusePrevention']
                self.password_policy['PasswordReusePrevention'] = True
            # There is a bug in the API: ExpirePasswords always returns false
            if 'MaxPasswordAge' in self.password_policy:
                self.password_policy['ExpirePasswords'] = True
        except Exception as e:
            if type(e) == botocore.exceptions.ClientError:
                if e.response['Error']['Code'] == 'NoSuchEntity':
                    self.password_policy = {}
                    self.password_policy['MinimumPasswordLength'] = '1' # As of 10/10/2016, 1-character passwords were authorized when no policy exists, even though the console displays 6
                    self.password_policy['RequireUppercaseCharacters'] = False
                    self.password_policy['RequireLowercaseCharacters'] = False
                    self.password_policy['RequireNumbers'] = False
                    self.password_policy['RequireSymbols'] = False
                    self.password_policy['PasswordReusePrevention'] = False
                    self.password_policy['ExpirePasswords'] = False
                else:
                    printError("Unexpected error: %s" % e)
            else:
                printError(str(e))



    ########################################
    ##### Roles
    ########################################
    def parse_roles(self, fetched_role, params):
        """
        Parse a single IAM role and fetch additional data
        """
        role = {}
        role['instances_count'] = 'N/A'
        # When resuming upon throttling error, skip if already fetched
        if fetched_role['RoleName'] in self.roles:
            return
        api_client = params['api_client']
        # Ensure consistent attribute names across resource types
        role['id'] = fetched_role.pop('RoleId')
        role['name'] = fetched_role.pop('RoleName')
        role['arn'] = fetched_role.pop('Arn')
        # Get other attributes
        get_keys(fetched_role, role, [ 'CreateDate', 'Path'])
        # Get role policies
        policies = self.__get_inline_policies(api_client, 'role', role['id'], role['name'])
        if len(policies):
            role['inline_policies'] = policies
        role['inline_policies_count'] = len(policies)
        # Get instance profiles
        profiles = handle_truncated_response(api_client.list_instance_profiles_for_role, {'RoleName': role['name']}, ['InstanceProfiles'])
        manage_dictionary(role, 'instance_profiles', {})
        for profile in profiles['InstanceProfiles']:
            manage_dictionary(role['instance_profiles'], profile['InstanceProfileId'], {})
            role['instance_profiles'][profile['InstanceProfileId']]['arn'] = profile['Arn']
            role['instance_profiles'][profile['InstanceProfileId']]['name'] = profile['InstanceProfileName']
        # Get trust relationship
        role['assume_role_policy'] = {}
        role['assume_role_policy']['PolicyDocument'] = fetched_role.pop('AssumeRolePolicyDocument')
        # Save role
        self.roles[role['id']] = role



    ########################################
    ##### Users
    ########################################
    def parse_users(self, user, params):
        """
        Parse a single IAM user and fetch additional data
        """
        if user['UserName'] in self.users:
            return
        api_client = params['api_client']
        # Ensure consistent attribute names across resource types
        user['id'] = user.pop('UserId')
        user['name'] = user.pop('UserName')
        user['arn'] = user.pop('Arn')
        policies = self.__get_inline_policies(api_client, 'user', user['id'], user['name'])
        if len(policies):
            user['inline_policies'] = policies
        user['inline_policies_count'] = len(policies)
        user['groups'] = []
        groups = handle_truncated_response(api_client.list_groups_for_user, {'UserName': user['name']}, ['Groups'])['Groups']
        for group in groups:
            user['groups'].append(group['GroupName'])
        try:
            user['LoginProfile'] = api_client.get_login_profile(UserName = user['name'])['LoginProfile']
        except Exception as e:
            pass
        user['AccessKeys'] = api_client.list_access_keys(UserName = user['name'])['AccessKeyMetadata']
        user['MFADevices'] = api_client.list_mfa_devices(UserName = user['name'])['MFADevices']
        self.users[user['id']] = user



    ########################################
    ##### Class helpers
    ########################################

    def get_id_for_resource(self, resource_type, resource_name):
        for resource_id in getattr(self, resource_type):
            if getattr(self, resource_type)[resource_id]['name'] == resource_name:
                return resource_id

    def __fetch_group_users(self, api_client, group_name):
        users = []
        fetched_users = api_client.get_group(GroupName = group_name)['Users']
        for user in fetched_users:
            users.append(user['UserId'])
        return users

    # TODO make this code shared (either for all classes or at least for global S3 and IAM)
    def __fetch_targets(self, api_client, target_type, list_params = {}):
        lower_target = target_type.lower()
        list_method = getattr(api_client, 'list_' + lower_target)
        targets = handle_truncated_response(list_method, list_params, [target_type])[target_type]
        setattr(self, '%s_count' % lower_target, len(targets))
        thread_work(targets, self.__fetch_target, params = {'api_client': api_client, 'target_type': lower_target[0:-1]}, num_threads = 10)
        self.__show_status(lower_target, True)

    def __fetch_target(self, q, params):
        api_client = params['api_client']
        method = getattr(self, 'parse_%s' % params['target_type'])
        while True:
            try:
                target = q.get()
                method(params, target)
            except Exception as e:
                printException(e)
            finally:
                q.task_done()

    def __show_status(self, target_type, newline = False):
        """
        Display fetching status to stdout
        """
        current = len(getattr(self, target_type))
        total = getattr(self, '%s_count' % target_type)
        sys.stdout.write("\r %s: %d/%d" % (target_type.title(), current, total))
        sys.stdout.flush()
        if newline:
            sys.stdout.write('\n')



    def finalize(self):
        """
        Formatting
        """
        # Github issue #99 - We expect a list of statements but policies with a single statement that is a dictionary are valid, make it a list locally
#        go_to_and_do(aws_config, aws_config['services']['iam'], ['groups', 'inline_policies', 'PolicyDocument'], ['services', 'iam'], enforce_list_of, {'attribute_name': 'Statement'})
#        go_to_and_do(aws_config, aws_config['services']['iam'], ['roles', 'inline_policies', 'PolicyDocument'], ['services', 'iam'], enforce_list_of, {'attribute_name': 'Statement'})
#        go_to_and_do(aws_config, aws_config['services']['iam'], ['roles', 'assume_role_policy.PolicyDocument' ], ['services', 'iam'], enforce_list_of, {'attribute_name': 'Statement'})
#        go_to_and_do(aws_config, aws_config['services']['iam'], ['roles', 'assume_role_policy.PolicyDocument.Statement', 'Principal' ], ['services', 'iam'], enforce_list_of, {'attribute_name': 'AWS'})
#        go_to_and_do(aws_config, aws_config['services']['iam'], ['users', 'inline_policies', 'PolicyDocument'], ['services', 'iam'], enforce_list_of, {'attribute_name': 'Statement'})
#        go_to_and_do(aws_config, aws_config['services']['iam'], ['managed_policies', 'PolicyDocument'], ['services', 'iam'], enforce_list_of, {'attribute_name': 'Statement'})


########################################
##### IAM functions
########################################


#
# If necessary, allows reformatting of attributes into a list
#
#def enforce_list_of(aws_config, current_config, path, current_path, resource_id, callback_args):
#    attribute_name = callback_args['attribute_name']
#    if resource_id == attribute_name and not type(current_config) == list:
#        # Current config is a copied structure, need to go back to the original and update
#        target = aws_config
#        for p in current_path:
#            target = target[p]
#        target[attribute_name] = [ target[attribute_name] 



def get_permissions(policy_document, permissions, resource_type, name, policy_name, is_managed_policy = False):
    manage_dictionary(permissions, 'Action', {})
    manage_dictionary(permissions, 'NotAction', {})
    if type(policy_document['Statement']) != list:
        parse_statement(policy_document, permissions, resource_type, name, policy_name, is_managed_policy, policy_document['Statement'])
    else:
        for statement in policy_document['Statement']:
            parse_statement(policy_document, permissions, resource_type, name, policy_name, is_managed_policy, statement)

def parse_statement(policy_document, permissions, resource_type, name, policy_name, is_managed_policy, statement):
        effect = str(statement['Effect'])
        action_string = 'Action' if 'Action' in statement else 'NotAction'
        resource_string = 'Resource' if 'Resource' in statement else 'NotResource'
        condition = statement['Condition'] if 'Condition' in statement else None
        parse_actions(permissions[action_string], statement[action_string], resource_string, statement[resource_string], effect, resource_type, name, policy_name, is_managed_policy, condition)

def parse_actions(permissions, actions, resource_string, resources, effect, resource_type, name, policy_name, is_managed_policy, condition):
    if type(actions) == list:
        for action in actions:
            parse_action(permissions, action, resource_string, resources, effect, resource_type, name, policy_name, is_managed_policy, condition)
    else:
        parse_action(permissions, actions, resource_string, resources, effect, resource_type, name, policy_name, is_managed_policy, condition)

def parse_action(permissions, action, resource_string, resources, effect, resource_type, name, policy_name, is_managed_policy, condition):
    manage_dictionary(permissions, action, {})
    parse_resources(permissions[action], resource_string, resources, effect, resource_type, name, policy_name, is_managed_policy, condition)

def parse_resources(permission, resource_string, resources, effect, resource_type, name, policy_name, is_managed_policy, condition):
    if type(resources) == list:
        for resource in resources:
            parse_resource(permission, resource_string, resource, effect, resource_type, name, policy_name, is_managed_policy, condition)
    else:
        parse_resource(permission, resource_string, resources, effect, resource_type, name, policy_name, is_managed_policy, condition)

def parse_resource(permission, resource_string, resource, effect, resource_type, name, policy_name, is_managed_policy, condition):
    manage_dictionary(permission, resource_type, {})
    manage_dictionary(permission[resource_type], effect, {})
    manage_dictionary(permission[resource_type][effect], name, {})
    manage_dictionary(permission[resource_type][effect][name], resource_string, {})
    manage_dictionary(permission[resource_type][effect][name][resource_string], resource, {})
    if is_managed_policy:
        policy_type = 'managed_policies'
    else:
        policy_type = 'inline_policies'
    manage_dictionary(permission[resource_type][effect][name][resource_string][resource], policy_type, {})
    manage_dictionary(permission[resource_type][effect][name][resource_string][resource][policy_type], policy_name, {})
    permission[resource_type][effect][name][resource_string][resource][policy_type][policy_name]['condition'] = condition





