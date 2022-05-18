from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.providers.gcp.resources.functions.utils import get_environment_secrets


class FunctionsV2(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_functions = await self.facade.functions.get_functions_v2(self.project_id)
        for raw_function in raw_functions:
            function_id, function = self._parse_function(raw_function)
            self[function_id] = function

    def _parse_function(self, raw_function):
        function_dict = {}

        function_dict['id'] = get_non_provider_id(raw_function['name'])
        function_dict['name'] = raw_function['name'].split('/')[-1]
        function_dict['status'] = raw_function['state']
        function_dict['update_time'] = raw_function['updateTime']
        function_dict['version_id'] = raw_function.get('serviceConfig', {}).get('revision')

        function_dict['runtime'] = raw_function.get('buildConfig', {}).get('runtime')
        function_dict['memory'] = raw_function.get('serviceConfig', {}).get('availableMemory')
        function_dict['timeout'] = raw_function.get('serviceConfig', {}).get('timeoutSeconds')
        function_dict['max_instances'] = raw_function.get('serviceConfig', {}).get('maxInstanceCount')

        function_dict['url'] = raw_function.get('serviceConfig', {}).get('uri')
        function_dict['ingress_settings'] = raw_function.get('serviceConfig', {}).get('ingressSettings')

        function_dict['service_account'] = raw_function.get('serviceConfig', {}).get('serviceAccountEmail')
        function_dict['bindings'] = raw_function['bindings']

        function_dict['environment_variables'] = raw_function.get('serviceConfig', {}).get('environmentVariables')
        function_dict['environment_variables_secrets'] = get_environment_secrets(function_dict['environment_variables'])

        function_dict['labels'] = raw_function['labels']

        return function_dict['id'], function_dict
