from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.basefacade import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils
from ScoutSuite.providers.utils import run_concurrently

class IAMFacade(GCPBaseFacade):
    def __init__(self):
        super(IAMFacade, self).__init__('iam', 'v1')

    async def get_bindings(self, project_id: str, service_account_email: str):
        try:
            resource = 'projects/{}/serviceAccounts/{}'.format(project_id, service_account_email)
            iam_client = self._get_client()
            response = await run_concurrently(
                    lambda: iam_client.projects().serviceAccounts().getIamPolicy(resource=resource).execute()
            )
            return response.get('bindings', [])
        except Exception as e:
            print_exception('Failed to retrieve service account IAM policy bindings: {}'.format(e))
            return []

    async def get_keys(self, project_id: str, service_account_email: str, key_types: list=[]):
        try:
            name = 'projects/{}/serviceAccounts/{}'.format(project_id, service_account_email)
            iam_client = self._get_client()
            response = await run_concurrently(
                    lambda: iam_client.projects().serviceAccounts().keys().list(name=name,
                                                                                keyTypes=key_types).execute()
            )
            return response.get('keys', [])
        except Exception as e:
            print_exception('Failed to retrieve service account keys: {}'.format(e))
            return []

    async def get_key(self, key_name: str):
        try:
            iam_client = self._get_client()
            response = await run_concurrently(
                lambda: iam_client.projects().serviceAccounts().keys().get(name=key_name,
                                                                           fields='').execute()
            )
            return response
        except Exception as e:
            print_exception('Failed to retrieve service account keys: {}'.format(e))
            return []

    async def get_service_accounts(self, project_id: str):
        try:
            name = 'projects/{}'.format(project_id)     
            iam_client = self._get_client()
            request = iam_client.projects().serviceAccounts().list(name=name)
            service_accounts_group = iam_client.projects().serviceAccounts()
            return await GCPFacadeUtils.get_all('accounts', request, service_accounts_group)
        except Exception as e:
            print_exception('Failed to retrieve service accounts: {}'.format(e))
            return []
