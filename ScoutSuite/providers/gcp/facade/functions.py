from google.cloud import kms
from google.api_core.gapic_v1.client_info import ClientInfo

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.basefacade import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.utils import get_user_agent


class FunctionsFacade(GCPBaseFacade):
    def __init__(self):
        # The version needs to be set per-function
        super().__init__('cloudfunctions', None)  # API Client


    async def get_functions_v1(self, project_id: str):
        results = await self.get_functions_version(project_id, "v1")
        return results

    async def get_functions_v2(self, project_id: str):
        results = await self.get_functions_version(project_id, "v2alpha")
        return results

    async def get_functions_version(self, project_id: str, api_version: str):
        try:
            functions_client = self._build_arbitrary_client(self._client_name, api_version, force_new=True)
            parent = f'projects/{project_id}/locations/-'
            functions = functions_client.projects().locations().functions()
            request = functions.list(parent=parent)
            results = await GCPFacadeUtils.get_all('functions', request, functions)
            return results

        except Exception as e:
            print_exception(f'Failed to retrieve Cloud Functions functions ({api_version}): {e}')
            return []
