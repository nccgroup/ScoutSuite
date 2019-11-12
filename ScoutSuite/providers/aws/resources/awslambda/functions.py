from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class Functions(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(Functions, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_functions = await self.facade.awslambda.get_functions(self.region)
        for raw_function in raw_functions:
            name, resource = self._parse_function(raw_function)
            self[name] = resource

    def _parse_function(self, raw_function):

        function_dict = {}
        function_dict['name'] = raw_function.get('FunctionName')
        function_dict['arn'] = raw_function.get('FunctionArn')
        function_dict['runtime'] = raw_function.get('Runtime')
        function_dict['role'] = raw_function.get('Role')
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
        return function_dict['name'], function_dict

