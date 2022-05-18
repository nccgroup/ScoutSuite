from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.basefacade import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils
from ScoutSuite.providers.utils import map_concurrently, run_concurrently, get_and_set_concurrently


class FunctionsFacade(GCPBaseFacade):
    def __init__(self):
        # The version needs to be set per-function
        super().__init__('cloudfunctions', None)  # API Client

    async def get_functions_v1(self, project_id: str):
        return await self._get_functions_version("v1", project_id)

    async def get_functions_v2(self, project_id: str):
        return await self._get_functions_version("v2alpha", project_id)

    async def _get_functions_version(self, api_version: str, project_id: str):
        try:
            # get list of functions
            list_results = await self._list_functions_version(project_id, api_version)
            # get list of function names
            functions_list = [function.get('name') for function in list_results]
        except Exception as e:
            print_exception(f'Failed to list Cloud Functions functions ({api_version}): {e}')
            return []
        else:
            functions = await map_concurrently(self._get_function_version, functions_list, api_version=api_version)
            await get_and_set_concurrently([self._get_and_set_function_iam_policy],
                                           functions,
                                           api_version=api_version)
            return functions

    async def _list_functions_version(self, project_id: str, api_version: str):
        functions_client = self._build_arbitrary_client(self._client_name, api_version, force_new=True)
        parent = f'projects/{project_id}/locations/-'
        functions = functions_client.projects().locations().functions()
        request = functions.list(parent=parent)
        results = await GCPFacadeUtils.get_all('functions', request, functions)
        return results

    async def _get_function_version(self, name: str, api_version: str):
        try:
            functions_client = self._build_arbitrary_client(self._client_name, api_version, force_new=True)
            functions = functions_client.projects().locations().functions()
            request = functions.get(name=name)
            return await run_concurrently(lambda: request.execute())
        except Exception as e:
            print_exception(f'Failed to get Cloud Functions functions ({api_version}): {e}')
            return {}

    async def _get_and_set_function_iam_policy(self, function, api_version: str):
        try:
            functions_client = self._build_arbitrary_client(self._client_name, api_version, force_new=True)
            functions = functions_client.projects().locations().functions()
            request = functions.getIamPolicy(resource=function.get('name'))
            policy = await run_concurrently(lambda: request.execute())
            # setattr(function, 'bindings', policy.get('bindings', []))
            function['bindings'] = policy.get('bindings', [])
        except Exception as e:
            print_exception(f'Failed to get bindings for Cloud Functions function {function.get("name")} '
                            f'({api_version}): {e}')
            function['bindings'] = []
