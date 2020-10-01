import asyncio
import functools

from botocore.exceptions import ClientError

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import get_non_provider_id, run_concurrently, get_and_set_concurrently


class IAMFacade(AWSBaseFacade):
    async def get_credential_reports(self):
        client = AWSFacadeUtils.get_client('iam', self.session)
        # When no credential report exists, we first need to initiate the creation of a new report by calling
        # client.generate_credential_report and then check for COMPLETE status before trying to download it:
        report_generated, n_attempts = False, 3
        try:
            while not report_generated and n_attempts > 0:
                response = await run_concurrently(client.generate_credential_report)
                if response['State'] == 'COMPLETE':
                    report_generated = True
                else:
                    n_attempts -= 1
                    await asyncio.sleep(0.1)  # Wait for 100ms before doing a new attempt.
        except Exception as e:
            print_exception(f'Failed to generate credential report: {e}')
            return []
        finally:
            if not report_generated and n_attempts == 0:
                print_exception(f'Failed to complete credential report generation in {n_attempts} attempts')
                return []

        try:
            report = await run_concurrently(lambda: client.get_credential_report()['Content'])

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
        except Exception as e:
            print_exception(f'Failed to download credential report: {e}')
            return []

    async def get_groups(self):
        groups = await AWSFacadeUtils.get_all_pages('iam', None, self.session, 'list_groups', 'Groups')
        await get_and_set_concurrently(
            [self._get_and_set_group_users,
             functools.partial(self._get_and_set_inline_policies, iam_resource_type='group')], groups)
        return groups

    async def get_policies(self):
        policies = await AWSFacadeUtils.get_all_pages(
            'iam', None, self.session, 'list_policies', 'Policies', OnlyAttached=True)
        await get_and_set_concurrently([self._get_and_set_policy_details], policies)
        return policies

    async def _get_and_set_policy_details(self, policy):
        client = AWSFacadeUtils.get_client('iam', self.session)
        try:
            policy_version = await run_concurrently(
                lambda: client.get_policy_version(PolicyArn=policy['Arn'], VersionId=policy['DefaultVersionId']))
            policy['PolicyDocument'] = policy_version['PolicyVersion']['Document']
        except Exception as e:
            print_exception(f'Failed to get policy version: {e}')
        else:
            policy['attached_to'] = {}
            attached_entities = await AWSFacadeUtils.get_multiple_entities_from_all_pages(
                'iam', None, self.session, 'list_entities_for_policy', ['PolicyGroups', 'PolicyRoles', 'PolicyUsers'],
                PolicyArn=policy['Arn'])

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

    async def get_users(self):
        users = await AWSFacadeUtils.get_all_pages('iam', None, self.session, 'list_users', 'Users')
        await get_and_set_concurrently(
            [functools.partial(self._get_and_set_inline_policies, iam_resource_type='user'),
             self._get_and_set_user_groups,
             self._get_and_set_user_tags,
             self._get_and_set_user_login_profile,
             self._get_and_set_user_access_keys,
             self._get_and_set_user_mfa_devices,
             self._get_and_set_user_tags],
            users)
        
        return users

    async def _get_and_set_user_login_profile(self, user: {}):
        client = AWSFacadeUtils.get_client('iam', self.session)
        try:
            user['LoginProfile'] = await run_concurrently(
                lambda: client.get_login_profile(UserName=user['UserName'])['LoginProfile'])
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchEntity":
                #  If the user has not been assigned a password, the operation returns a 404 (NoSuchEntity ) error.
                pass
            else:
                print_exception(f'Failed to get login profile: {e}')
        except Exception as e:
            print_exception(f'Failed to get login profile: {e}')

    async def _get_and_set_user_groups(self, user: {}):
        groups = await AWSFacadeUtils.get_all_pages(
            'iam', None, self.session, 'list_groups_for_user', 'Groups', UserName=user['UserName'])
        user['groups'] = [group['GroupName'] for group in groups]

    async def _get_and_set_user_tags(self, user: {}):
        client = AWSFacadeUtils.get_client('iam', self.session)
        try:
            user_tagset = await run_concurrently(lambda: client.list_user_tags(UserName=user['UserName']))
            user['tags'] = {x['Key']: x['Value'] for x in user_tagset['Tags']}
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchEntity":
                #  If the user has not been assigned tags, the operation returns a 404 (NoSuchEntity ) error.
                pass
            else:
                print_exception('Failed to get user tags: {}'.format(e))
        except Exception as e:
            print_exception('Failed to get user tags: {}'.format(e))
        
    async def get_roles(self):
        roles = await AWSFacadeUtils.get_all_pages('iam', None, self.session, 'list_roles', 'Roles')
        for role in roles:
            role['instances_count'] = 'N/A'
            # Get trust relationship
            role['assume_role_policy'] = {}
            role['assume_role_policy']['PolicyDocument'] = role.pop(
                'AssumeRolePolicyDocument')
        await get_and_set_concurrently(
            [functools.partial(self._get_and_set_inline_policies, iam_resource_type='role'),
             self._get_and_set_role_profiles,
             self._get_and_set_role_tags], roles)

        return roles

    async def _get_and_set_role_tags(self, role: {}):
        client = AWSFacadeUtils.get_client('iam', self.session)
        try:
            role_tagset = await run_concurrently(lambda: client.list_role_tags(RoleName=role['RoleName']))
            role['tags'] = {x['Key']: x['Value'] for x in role_tagset['Tags']}
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchEntity":
                #  If the user has not been assigned tags, the operation returns a 404 (NoSuchEntity ) error.
                pass
            else:
                print_exception('Failed to get role tags: {}'.format(e))
        except Exception as e:
            print_exception('Failed to get role tags: {}'.format(e))


    async def _get_and_set_role_profiles(self, role: {}):
        profiles = await AWSFacadeUtils.get_all_pages(
            'iam', None, self.session, 'list_instance_profiles_for_role', 'InstanceProfiles',
            RoleName=role['RoleName'])
        role.setdefault('instance_profiles', {})
        for profile in profiles:
            profile_id = profile['InstanceProfileId']
            role['instance_profiles'].setdefault(profile_id, {})
            role['instance_profiles'][profile_id].setdefault(
                'arn', profile['Arn'])
            role['instance_profiles'][profile_id].setdefault(
                'name', profile['InstanceProfileName'])

    async def get_password_policy(self):
        client = AWSFacadeUtils.get_client('iam', self.session)
        try:
            return (await run_concurrently(client.get_account_password_policy))['PasswordPolicy']
        except ClientError as e:
            if e.response['Error']['Code'] != 'NoSuchEntity':
                print_exception(f'Failed to get account password policy: {e}')
            return None

    async def _get_and_set_user_access_keys(self, user: {}):
        client = AWSFacadeUtils.get_client('iam', self.session)
        try:
            user['AccessKeys'] = await run_concurrently(
                lambda: client.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata'])
        except Exception as e:
            print_exception(f'Failed to list access keys: {e}')

    async def _get_and_set_user_mfa_devices(self, user: {}):
        user['MFADevices'] = await self.get_user_mfa_devices(user['UserName'])

    async def get_user_mfa_devices(self, username: str):
        client = AWSFacadeUtils.get_client('iam', self.session)
        try:
            return await run_concurrently(
                lambda: client.list_mfa_devices(UserName=username)['MFADevices'])
        except Exception as e:
            print_exception(f'Failed to list MFA devices for user: {e}')

    async def get_virtual_mfa_devices(self):
        client = AWSFacadeUtils.get_client('iam', self.session)
        try:
            return await run_concurrently(
                lambda: client.list_virtual_mfa_devices()['VirtualMFADevices'])
        except Exception as e:
            print_exception(f'Failed to list virtual MFA devices: {e}')

    async def _get_and_set_group_users(self, group: {}):
        client = AWSFacadeUtils.get_client('iam', self.session)
        try:
            users = await run_concurrently(lambda: client.get_group(GroupName=group['GroupName'])['Users'])
            group['Users'] = [user['UserId'] for user in users]
        except Exception as e:
            print_exception('Failed to get IAM group {}: {}'.format(group['GroupName'], e))

    async def _get_and_set_inline_policies(self, resource, iam_resource_type):
        client = AWSFacadeUtils.get_client('iam', self.session)
        list_policy_method = getattr(client, 'list_' + iam_resource_type + '_policies')
        resource_name = resource[iam_resource_type.title() + 'Name']
        args = {iam_resource_type.title() + 'Name': resource_name}

        resource['inline_policies'] = {}

        try:
            policy_names = await run_concurrently(lambda: list_policy_method(**args)['PolicyNames'])
            if len(policy_names) == 0:
                resource['inline_policies_count'] = 0
        except Exception as e:
            print_exception(f'Failed to list IAM policy: {e}')
        else:
            get_policy_method = getattr(client, 'get_' + iam_resource_type + '_policy')
            try:
                tasks = {
                    asyncio.ensure_future(
                        run_concurrently(lambda policy_name=policy_name:
                                         get_policy_method(**dict(args, PolicyName=policy_name)))
                    ) for policy_name in policy_names
                }
            except Exception as e:
                print_exception(f'Failed to get policy methods: {e}')
            else:
                for task in asyncio.as_completed(tasks):
                    policy = await task
                    policy_name = policy['PolicyName']
                    policy_id = get_non_provider_id(policy_name)
                    policy_document = policy['PolicyDocument']

                    resource['inline_policies'][policy_id] = {}
                    resource['inline_policies'][policy_id]['PolicyDocument'] = self._normalize_statements(
                        policy_document)
                    resource['inline_policies'][policy_id]['name'] = policy_name
                resource['inline_policies_count'] = len(resource['inline_policies'])

    def _normalize_statements(self, policy_document):
        if policy_document:
            if type(policy_document['Statement']) == list:
                pass
                # for statement in policy_document['Statement']:
                #     statement = self._normalize_single_statement(statement)
            elif type(policy_document['Statement']) == dict:
                policy_document['Statement'] = self._normalize_single_statement(policy_document['Statement'])
            else:
                print_exception('Failed to normalize policy document')
        return policy_document

    def _normalize_single_statement(self, statement):
        # Action or NotAction
        action_string = 'Action' if 'Action' in statement else 'NotAction'
        if type(statement[action_string]) != list:
            statement[action_string] = [statement[action_string]]
        # Resource or NotResource
        resource_string = 'Resource' if 'Resource' in statement else 'NotResource'
        if type(statement[resource_string]) != list:
            statement[resource_string] = [statement[resource_string]]
        # Result
        return statement

