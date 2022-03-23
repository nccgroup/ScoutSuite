import json

from ScoutSuite.core.console import print_exception, print_warning
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class LambdaFacade(AWSBaseFacade):
    async def get_functions(self, region):
        try:
            return await AWSFacadeUtils.get_all_pages('lambda', region, self.session, 'list_functions', 'Functions')
        except Exception as e:
            print_exception(f'Failed to get Lambda functions: {e}')
            return []

    async def get_access_policy(self, function_name, region):
        client = AWSFacadeUtils.get_client('lambda', self.session, region)
        try:
            policy = client.get_policy(FunctionName=function_name)
            if policy is not None and 'Policy' in policy:
                return json.loads(policy['Policy'])
        except Exception as e:
            # If there's no policy, it will return this exception. Hence why we ignore.
            if "ResourceNotFoundException" not in str(e):
                print_exception('Failed to get Lambda access policy: {}'.format(e))
            return None

    async def get_role_with_managed_policies(self, role_name):
        client = AWSFacadeUtils.get_client('iam', self.session)
        try:
            role = client.get_role(RoleName=role_name)['Role']
            managed_policies = client.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
            for policy in managed_policies:
                policy_version = client.get_policy(PolicyArn=policy['PolicyArn'])
                if 'Policy' in policy_version and 'DefaultVersionId' in policy_version['Policy']:
                    policy_version = policy_version['Policy']['DefaultVersionId']
                    document = client.get_policy_version(PolicyArn=policy['PolicyArn'], VersionId=policy_version)
                    if 'PolicyVersion' in document and 'Document' in document['PolicyVersion']:
                        policy['Document'] = document['PolicyVersion']['Document']
            role['policies'] = managed_policies
            return role
        except Exception as e:
            if 'NoSuchEntity' in str(e):
                print_warning(f'Failed to get role from managed policies: {e}')
            else:
                print_exception(f'Failed to get role from managed policies: {e}')
            return None

    async def get_env_variables(self, function_name, region):
        client = AWSFacadeUtils.get_client('lambda', self.session, region)
        try:
            function_configuration = client.get_function_configuration(FunctionName=function_name)
            if "Environment" in function_configuration and "Variables" in function_configuration["Environment"]:
                return function_configuration["Environment"]["Variables"]
        except Exception as e:
            if 'ResourceNotFoundException' in str(e):
                print_warning('Failed to get Lambda function configuration: {}'.format(e))
            else:
                print_exception('Failed to get Lambda function configuration: {}'.format(e))
        return []

