# -*- coding: utf-8 -*-

from opinel.utils.aws import connect_service, handle_truncated_response
from opinel.utils.console import printError, printException
from opinel.utils.globals import manage_dictionary

from AWSScout2.configs.base import BaseConfig
from AWSScout2.utils import *

from botocore.exceptions import ClientError


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
        ('policies', 'Policies', 'list_policies', [ {'Scope': 'Local'}, {'OnlyAttached': True} ], False),
        ('roles', 'Roles', 'list_roles', {}, False),
        ('users', 'Users', 'list_users', {}, False),
        ('credential_report', '', '', {}, False),
        ('password_policy', '', '', {}, False)
        # TODO: Federations
        # TODO: KMS ?
    )

    def __init__(self, target_config):
        self.credential_report = {}
        self.groups = {}
        self.password_policy = {}
        self.permissions = {}
        self.policies = {}
        self.roles = {}
        self.users = {}
        super(IAMConfig, self).__init__(target_config)



    ########################################
    ##### Overload to fetch credentials report before and after
    ########################################
    def fetch_all(self, credentials, regions=[], partition_name='aws', targets=None):
        self.fetch_credential_report(credentials, True)
        super(IAMConfig, self).fetch_all(credentials, regions, partition_name, targets)
        self.fetch_password_policy(credentials)
        self.fetch_credential_report(credentials)
        self.fetchstatuslogger.show(True)



    ########################################
    ##### Credential report
    ########################################
    def fetch_credential_report(self, credentials, ignore_exception = False):
        """
        Fetch the credential report

        :param: api_client
        :type: FOO
        :param: ignore_exception : initiate credential report creation as not  always ready
        :type: Boolean
        """
        iam_report = {}
        try:
            api_client = connect_service('iam', credentials, silent = True)
            response = api_client.generate_credential_report()
            if response['State'] != 'COMPLETE':
                if not ignore_exception:
                    printError('Failed to generate a credential report.')
                return
            report = api_client.get_credential_report()['Content']
            lines = report.splitlines()
            keys = lines[0].decode('utf-8').split(',')
            for line in lines[1:]:
                values = line.decode('utf-8').split(',')
                manage_dictionary(iam_report, values[0], {})
                for key, value in zip(keys, values):
                    iam_report[values[0]][key] = value
            self.credential_report = iam_report
            self.fetchstatuslogger.counts['credential_report']['fetched'] = 1
        except Exception as e:
            if ignore_exception:
                return
            printError('Failed to download a credential report.')
            printException(e)



    ########################################
    ##### Groups
    ########################################
    def parse_groups(self, group, params):
        """
        Parse a single IAM group and fetch additional information
        """
        # When resuming upon throttling error, skip if already fetched
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
                policy['attached_to'][resource_type].append({'name': resource_name})
        # Save policy
        self.policies[policy['id']] = policy



    ########################################
    ##### Password policy
    ########################################
    def fetch_password_policy(self, credentials):
        """
        Fetch the password policy that applies to all IAM users within the AWS account
        """
        self.fetchstatuslogger.counts['password_policy']['discovered'] = 0
        self.fetchstatuslogger.counts['password_policy']['fetched'] = 0
        try:
            api_client = connect_service('iam', credentials, silent = True)
            self.password_policy = api_client.get_account_password_policy()['PasswordPolicy']
            if 'PasswordReusePrevention' not in self.password_policy:
                self.password_policy['PasswordReusePrevention'] = False
            else:
                self.password_policy['PreviousPasswordPrevented'] = self.password_policy['PasswordReusePrevention']
                self.password_policy['PasswordReusePrevention'] = True
            # There is a bug in the API: ExpirePasswords always returns false
            if 'MaxPasswordAge' in self.password_policy:
                self.password_policy['ExpirePasswords'] = True
            self.fetchstatuslogger.counts['password_policy']['discovered'] = 1
            self.fetchstatuslogger.counts['password_policy']['fetched'] = 1

        except ClientError as e:
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
                raise e
        except Exception as e:
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
        # TODO: Users signing certss
        self.users[user['id']] = user



    ########################################
    ##### Finalize IAM config
    ########################################
    def finalize(self):
        # Update permissions for managed policies
        for policy_id in self.policies:
            if 'attached_to' in self.policies[policy_id] and len(self.policies[policy_id]['attached_to']) > 0:
                for entity_type in self.policies[policy_id]['attached_to']:
                    for entity in self.policies[policy_id]['attached_to'][entity_type]:
                        entity['id'] = self.get_id_for_resource(entity_type, entity['name'])
                        entities = getattr(self, entity_type)
                        manage_dictionary(entities[entity['id']], 'policies', [])
                        manage_dictionary(entities[entity['id']], 'policies_counts', 0)
                        entities[entity['id']]['policies'].append(policy_id)
                        entities[entity['id']]['policies_counts'] += 1
                        self.__parse_permissions(policy_id, self.policies[policy_id]['PolicyDocument'], 'policies', entity_type, entity['id'])
            else:
                self.__parse_permissions(policy_id, self.policies[policy_id]['PolicyDocument'], 'policies', None, None)
        super(IAMConfig, self).finalize()



    ########################################
    ##### Class helpers
    ########################################

    def get_id_for_resource(self, iam_resource_type, resource_name):
        for resource_id in getattr(self, iam_resource_type):
            if getattr(self, iam_resource_type)[resource_id]['name'] == resource_name:
                return resource_id


    def __fetch_group_users(self, api_client, group_name):
        users = []
        fetched_users = api_client.get_group(GroupName = group_name)['Users']
        for user in fetched_users:
            users.append(user['UserId'])
        return users


    ########################################
    ##### Inline policies
    ########################################
    def __get_inline_policies(self, api_client, iam_resource_type, resource_id, resource_name):
        fetched_policies = {}
        get_policy_method = getattr(api_client, 'get_' + iam_resource_type + '_policy')
        list_policy_method = getattr(api_client, 'list_' + iam_resource_type + '_policies')
        args = {}
        args[iam_resource_type.title() + 'Name'] = resource_name
        try:
            policy_names = list_policy_method(**args)['PolicyNames']
        except Exception as e:
            if is_throttled(e):
                raise e
            else:
                printException(e)
                return fetched_policies
        try:
            for policy_name in policy_names:
                args['PolicyName'] = policy_name
                policy_document = get_policy_method(**args)['PolicyDocument']
                policy_id = self.get_non_aws_id(policy_name)
                manage_dictionary(fetched_policies, policy_id, {})
                fetched_policies[policy_id]['PolicyDocument'] = policy_document
                fetched_policies[policy_id]['name'] = policy_name
                self.__parse_permissions(policy_id, policy_document, 'inline_policies', iam_resource_type + 's', resource_id)
        except Exception as e:
            if is_throttled(e):
                raise e
            else:
                printException(e)
        return fetched_policies


    def __parse_permissions(self, policy_name, policy_document, policy_type, iam_resource_type, resource_name):
        # Enforce list of statements (Github issue #99)
        if type(policy_document['Statement']) != list:
            policy_document['Statement'] = [ policy_document['Statement'] ]
        for statement in policy_document['Statement']:
            self.__parse_statement(policy_name, statement, policy_type, iam_resource_type, resource_name)


    def __parse_statement(self, policy_name, statement, policy_type, iam_resource_type, resource_name):
            # Effect
            effect = str(statement['Effect'])
            # Action or NotAction
            action_string = 'Action' if 'Action' in statement else 'NotAction'
            if type(statement[action_string]) != list:
                statement[action_string] = [ statement[action_string] ]
            # Resource or NotResource
            resource_string = 'Resource' if 'Resource' in statement else 'NotResource'
            if type(statement[resource_string]) != list:
                statement[resource_string] = [ statement[resource_string] ]
            # Condition
            condition = statement['Condition'] if 'Condition' in statement else None
            manage_dictionary(self.permissions, action_string, {})
            if iam_resource_type == None:
                return
            self.__parse_actions(effect, action_string, statement[action_string], resource_string, statement[resource_string], iam_resource_type, resource_name, policy_name, policy_type, condition)


    def __parse_actions(self, effect, action_string, actions, resource_string, resources, iam_resource_type, iam_resource_name, policy_name, policy_type, condition):
        for action in actions:
            manage_dictionary(self.permissions[action_string], action, {})
            manage_dictionary(self.permissions[action_string][action], iam_resource_type, {})
            manage_dictionary(self.permissions[action_string][action][iam_resource_type], effect, {})
            manage_dictionary(self.permissions[action_string][action][iam_resource_type][effect], iam_resource_name, {})
            self.__parse_action(effect, action_string, action, resource_string, resources, iam_resource_type, iam_resource_name, policy_name, policy_type, condition)


    def __parse_action(self, effect, action_string, action, resource_string, resources, iam_resource_type, iam_resource_name, policy_name, policy_type, condition):
        for resource in resources:
            self.__parse_resource(effect, action_string, action, resource_string, resource, iam_resource_type, iam_resource_name, policy_name, policy_type, condition)


    def __parse_resource(self, effect, action_string, action, resource_string, resource, iam_resource_type, iam_resource_name, policy_name, policy_type, condition):
        manage_dictionary(self.permissions[action_string][action][iam_resource_type][effect][iam_resource_name], resource_string, {})
        manage_dictionary(self.permissions[action_string][action][iam_resource_type][effect][iam_resource_name][resource_string], resource, {})
        manage_dictionary(self.permissions[action_string][action][iam_resource_type][effect][iam_resource_name][resource_string][resource], policy_type, {})
        manage_dictionary(self.permissions[action_string][action][iam_resource_type][effect][iam_resource_name][resource_string][resource][policy_type], policy_name, {})
        self.permissions[action_string][action][iam_resource_type][effect][iam_resource_name][resource_string][resource][policy_type][policy_name]['condition'] = condition
