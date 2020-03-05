from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class Functions(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(Functions, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_functions = await self.facade.awslambda.get_functions(self.region)
        for raw_function in raw_functions:
            name, resource = await self._parse_function(raw_function)
            self[name] = resource

    async def _parse_function(self, raw_function):

        function_dict = {}
        function_dict['name'] = raw_function.get('FunctionName')
        function_dict['arn'] = raw_function.get('FunctionArn')
        function_dict['runtime'] = raw_function.get('Runtime')
        function_dict['handler'] = raw_function.get('Handler')
        function_dict['code_size'] = raw_function.get('CodeSize')
        function_dict['description'] = raw_function.get('Description')
        function_dict['timeout'] = raw_function.get('Timeout')
        function_dict['memory_size'] = raw_function.get('MemorySize')
        function_dict['last_modified'] = raw_function.get('LastModified')
        function_dict['code_sha256'] = raw_function.get('CodeSha256')
        function_dict['version'] = raw_function.get('Version')
        function_dict['tracing_config'] = raw_function.get('TracingConfig')
        function_dict['revision_id'] = raw_function.get('RevisionId')

        await self._add_role_information(function_dict, raw_function.get('Role'))
        await self._add_access_policy_information(function_dict)

        return function_dict['name'], function_dict

    async def _add_role_information(self, function_dict, role_id):
        function_dict['role_arn'] = role_id
        role_name = role_id.split("/")[-1]
        function_dict['execution_role'] = await self.facade.iam.get_role_with_managed_policies(role_name)
        # Make it easier to build rules based on policies attached to execution roles
        statements = []
        for policy in function_dict['execution_role']['policies']:
            if 'Document' in policy and 'Statement' in policy['Document']:
                statements += policy['Document']['Statement']
        function_dict['execution_role']['policy_statements'] = statements

    async def _add_access_policy_information(self, function_dict):
        access_policy = await self.facade.awslambda.get_access_policy(function_dict['name'], self.region)
        if access_policy:
            # Make it easier to build rules based on allowed principals
            allowed_principals = []
            for statement in access_policy['Statement']:
                if statement['Effect'] == 'Allow':
                    allowed_principals += [statement['Principal']]
            access_policy['allowed_principals'] = allowed_principals
            function_dict["access_policy"] = access_policy
        else:
            function_dict["access_policy"] = {"allowed_principals": []}
