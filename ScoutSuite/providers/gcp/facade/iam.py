from googleapiclient import discovery
from ScoutSuite.providers.gcp.utils import MemoryCache
from ScoutSuite.providers.gcp.facade.facade import Facade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils

class IAMFacade(Facade):
    def _build_client(self):
        return discovery.build('iam', 'v1', cache_discovery=False, cache=MemoryCache())

    # TODO: Make truly async
    async def get_bindings(self, project_id, service_account_email):
        resource = 'projects/{}/serviceAccounts/{}'.format(project_id, service_account_email)
        iam_client = self._get_client()
        response = iam_client.projects().serviceAccounts().getIamPolicy(resource=resource).execute()
        return response.get('bindings', [])

    # TODO: Make truly async
    async def get_keys(self, project_id, service_account_email):
        name = 'projects/{}/serviceAccounts/{}'.format(project_id, service_account_email)
        iam_client = self._get_client()
        response = iam_client.projects().serviceAccounts().keys().list(name=name).execute()
        return response.get('keys', [])

    # TODO: Make truly async
    async def get_service_accounts(self, project_id):
        name = 'projects/{}'.format(project_id)     
        iam_client = self._get_client()
        request = iam_client.projects().serviceAccounts().list(name=name)
        service_accounts_group = iam_client.projects().serviceAccounts()
        return await GCPFacadeUtils.get_all('accounts', request, service_accounts_group)
