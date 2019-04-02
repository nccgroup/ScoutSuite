from ScoutSuite.providers.gcp.facade.base import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils
from ScoutSuite.providers.utils import run_concurrently

class IAMFacade(GCPBaseFacade):
    def __init__(self):
        super(IAMFacade, self).__init__('iam', 'v1')

    async def get_bindings(self, project_id: str, service_account_email: str):
        resource = 'projects/{}/serviceAccounts/{}'.format(project_id, service_account_email)
        iam_client = self._get_client()
        response = await run_concurrently(
                lambda: iam_client.projects().serviceAccounts().getIamPolicy(resource=resource).execute()
        )
        return response.get('bindings', [])

    async def get_keys(self, project_id: str, service_account_email: str):
        name = 'projects/{}/serviceAccounts/{}'.format(project_id, service_account_email)
        iam_client = self._get_client()
        response = await run_concurrently(
                lambda: iam_client.projects().serviceAccounts().keys().list(name=name).execute()
        )
        return response.get('keys', [])

    async def get_service_accounts(self, project_id: str):
        name = 'projects/{}'.format(project_id)     
        iam_client = self._get_client()
        request = iam_client.projects().serviceAccounts().list(name=name)
        service_accounts_group = iam_client.projects().serviceAccounts()
        return await GCPFacadeUtils.get_all('accounts', request, service_accounts_group)
