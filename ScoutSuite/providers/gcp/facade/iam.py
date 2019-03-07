from googleapiclient import discovery
from ScoutSuite.providers.gcp.utils import MemoryCache

class IAMFacade:
    def __init__(self):
        self._iam_client = discovery.build('iam', 'v1', cache_discovery=False, cache=MemoryCache())

    # TODO: Make truly async
    async def get_bindings(self, project_id, service_account_email):
        resource = f'projects/{project_id}/serviceAccounts/{service_account_email}'
        return self._iam_client.projects().serviceAccounts().getIamPolicy(resource=resource).execute()

    # TODO: Make truly async
    async def get_keys(self, project_id, service_account_email):
        name = f'projects/{project_id}/serviceAccounts/{service_account_email}'
        return self._iam_client.projects().serviceAccounts().keys().list(name=name).execute()

    # TODO: Make truly async
    async def get_service_accounts(self, project_id):
        name = f'projects/{project_id}'
        service_accounts = []      
        request = self._iam_client.projects().serviceAccounts().list(name=name)
        while request is not None:
            response = request.execute()
            service_accounts.extend(response.get('accounts', []))
            request = self._iam_client.projects().serviceAccounts().list_next(previous_request=request, previous_response=response)    
        return service_accounts
