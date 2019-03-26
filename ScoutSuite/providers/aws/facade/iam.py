from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.core.console import print_error, print_exception
from ScoutSuite.providers.utils import run_concurrently, get_non_provider_id
from ScoutSuite.providers.aws.utils import is_throttled
from ScoutSuite.providers.utils import run_concurrently, run_tasks_concurrently


class IAMFacade(AWSBaseFacade):
    async def get_credential_reports(self):
        client = AWSFacadeUtils.get_client('iam', self.session)
        response = await run_concurrently(client.generate_credential_report)

        if response['State'] != 'COMPLETE':
            print_error('Failed to generate a credential report.')
            return []

        report = (await run_concurrently(client.get_credential_report))['Content']

        # The report is a CSV string. The first row contains the name of each column. The next rows
        # each represent an individual account. This algorithm provides a simple initial parsing.
        lines = report.splitlines()
        keys = lines[0].decode('utf-8').split(',')

        credential_reports = []
        for line in lines[1:]:
            credential_report = {}
            values = line.decode('utf-8').split(',')
            for key, value in zip(keys, values):
                credential_report[key] = value

            credential_reports.append(credential_report)

        return credential_reports

    async def get_groups(self):
        groups = await AWSFacadeUtils.get_all_pages('iam', None, self.session, 'list_groups', 'Groups')
        for group in groups:
            group['Users'] = await self._fetch_group_users(group['GroupName'])
            policies = self._get_inline_policies(
                'group', group['GroupId'], group['GroupName'])
            if len(policies):
                group['inline_policies'] = policies
            group['inline_policies_count'] = len(policies)
        return groups

    async def get_policies(self):
        policies = await AWSFacadeUtils.get_all_pages('iam', None, self.session, 'list_policies', 'Policies', OnlyAttached=True)
        return await run_tasks_concurrently({
            self.get_detailed_policy(policy) for policy in policies
        })

    async def get_detailed_policy(self, policy):
        client = AWSFacadeUtils.get_client('iam', self.session)
        policy_version = await run_concurrently(lambda: client.get_policy_version(PolicyArn=policy['Arn'], VersionId=policy['DefaultVersionId']))
        policy['PolicyDocument'] = policy_version['PolicyVersion']['Document']

        policy['attached_to'] = {}
        attached_entities = await AWSFacadeUtils.get_multiple_entities_from_all_pages('iam', None, self.session, 'list_entities_for_policy',  ['PolicyGroups', 'PolicyRoles', 'PolicyUsers'], PolicyArn=policy['Arn'])

        for entity_type in attached_entities:
            resource_type = entity_type.replace('Policy', '').lower()
            if len(attached_entities[entity_type]):
                policy['attached_to'][resource_type] = []

            for entity in attached_entities[entity_type]:
                name_field = entity_type.replace('Policy', '')[
                    :-1] + 'Name'
                resource_name = entity[name_field]
                id_field = entity_type.replace('Policy', '')[:-1] + 'Id'
                resource_id = entity[id_field]
                policy['attached_to'][resource_type].append(
                    {'name': resource_name, 'id': resource_id})

        return policy

    async def get_users(self):
        users = await AWSFacadeUtils.get_all_pages('iam', None, self.session, 'list_users', 'Users')
        return await run_tasks_concurrently({
            self.get_detailed_user(user) for user in users
        })

    async def get_detailed_user(self, user):
        client = AWSFacadeUtils.get_client('iam', self.session)
        user_name = user['UserName']
        user_id = user['UserId']

        policies = self._get_inline_policies('user', user_id, user_name)
        if len(policies):
            user['inline_policies'] = policies
        user['inline_policies_count'] = len(policies)
        user['groups'] = []
        groups = await AWSFacadeUtils.get_all_pages('iam', None, self.session, 'list_groups_for_user', 'Groups', UserName=user_name)
        for group in groups:
            user['groups'].append(group['GroupName'])
        try:
            user['LoginProfile'] = await run_concurrently(
                lambda: client.get_login_profile(UserName=user_name)['LoginProfile'])
        except Exception:
            pass
        user['AccessKeys'] = await self._get_user_acces_keys(user_name)
        user['MFADevices'] = await self._get_user_mfa_devices(user_name)

        return user

    async def get_roles(self):
        roles = await AWSFacadeUtils.get_all_pages('iam', None, self.session, 'list_roles', 'Roles')

        # Handle throttling errors
        for role in roles:
            role['instances_count'] = 'N/A'

            # Get role policies
            policies = self._get_inline_policies(
                'role', role['RoleId'], role['RoleName'])
            if len(policies):
                role['inline_policies'] = policies
            role['inline_policies_count'] = len(policies)

            # Get instance profiles
            profiles = await AWSFacadeUtils.get_all_pages('iam', None, self.session, 'list_instance_profiles_for_role', 'InstanceProfiles', RoleName=role['RoleName'])
            role.setdefault('instance_profiles', {})
            for profile in profiles:
                profile_id = profile['InstanceProfileId']
                role['instance_profiles'].setdefault(profile_id, {})
                role['instance_profiles'][profile_id].setdefault(
                    'arn', profile['Arn'])
                role['instance_profiles'][profile_id].setdefault(
                    'name', profile['InstanceProfileName'])

            # Get trust relationship
            role['assume_role_policy'] = {}
            role['assume_role_policy']['PolicyDocument'] = role.pop(
                'AssumeRolePolicyDocument')

        return roles

    async def get_password_policy(self):
        client = AWSFacadeUtils.get_client('iam', self.session)
        return (await run_concurrently(client.get_account_password_policy))['PasswordPolicy']

    async def _get_user_acces_keys(self, user_name):
        client = AWSFacadeUtils.get_client('iam', self.session)
        response = await run_concurrently(lambda: client.list_access_keys(UserName=user_name))
        return response['AccessKeyMetadata']

    async def _get_user_mfa_devices(self, user_name):
        client = AWSFacadeUtils.get_client('iam', self.session)
        response = await run_concurrently(lambda: client.list_mfa_devices(UserName=user_name))
        return response['MFADevices']

    async def _fetch_group_users(self, group_name):
        client = AWSFacadeUtils.get_client('iam', self.session)
        fetched_users = client.get_group(GroupName=group_name)['Users']

        users = []
        for user in fetched_users:
            users.append(user['UserId'])
        return users

    async def _get_inline_policies(self, iam_resource_type, resource_id, resource_name):
        client = AWSFacadeUtils.get_client('iam', self.session)
        get_policy_method = getattr(
            client, 'get_' + iam_resource_type + '_policy')
        fetched_policies = {}
        list_policy_method = getattr(
            client, 'list_' + iam_resource_type + '_policies')
        args = {iam_resource_type.title() + 'Name': resource_name}
        
        try:
            policy_names = await run_concurrently(lambda: list_policy_method(**args)['PolicyNames'])
        except Exception as e:
            if is_throttled(e):
                raise e
            else:
                print_exception(e)
                return fetched_policies
        
        try:
            for policy_name in policy_names:
                args['PolicyName'] = policy_name
                policy_document = get_policy_method(**args)['PolicyDocument']
                policy_id = get_non_provider_id(policy_name)
                fetched_policies[policy_id] = {}
                fetched_policies[policy_id]['PolicyDocument'] = self._normalize_statements(
                    policy_document)
                fetched_policies[policy_id]['name'] = policy_name
                fetched_policies[policy_id] = fetched_policies[policy_id]
        except Exception as e:
            if is_throttled(e):
                raise e
            else:
                print_exception(e)

        return fetched_policies

    def _normalize_statements(self, policy_document):
        for statement in policy_document['Statement']:
            # Action or NotAction
            action_string = 'Action' if 'Action' in statement else 'NotAction'
            if type(statement[action_string]) != list:
                statement[action_string] = [statement[action_string]]
            # Resource or NotResource
            resource_string = 'Resource' if 'Resource' in statement else 'NotResource'
            if type(statement[resource_string]) != list:
                statement[resource_string] = [statement[resource_string]]

        return policy_document
