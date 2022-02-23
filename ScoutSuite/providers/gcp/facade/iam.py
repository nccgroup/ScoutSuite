from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.basefacade import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils
from ScoutSuite.providers.utils import run_concurrently

class IAMFacade(GCPBaseFacade):
    def __init__(self):
        super().__init__('iam', 'v1')

    async def get_service_accounts(self, project_id: str):
        try:
            name = f'projects/{project_id}'
            iam_client = self._get_client()
            request = iam_client.projects().serviceAccounts().list(name=name)
            service_accounts_group = iam_client.projects().serviceAccounts()
            return await GCPFacadeUtils.get_all('accounts', request, service_accounts_group)
        except Exception as e:
            print_exception(f'Failed to retrieve service accounts: {e}')
            return []

    async def get_service_account_bindings(self, project_id: str, service_account_email: str):
        try:
            resource = f'projects/{project_id}/serviceAccounts/{service_account_email}'
            iam_client = self._get_client()
            response = await run_concurrently(
                    lambda: iam_client.projects().serviceAccounts().getIamPolicy(resource=resource).execute()
            )
            return response.get('bindings', [])
        except Exception as e:
            print_exception(f'Failed to retrieve service account IAM policy bindings: {e}')
            return []

    async def get_service_account_keys(self, project_id: str, service_account_email: str, key_types: list=[]):
        try:
            name = f'projects/{project_id}/serviceAccounts/{service_account_email}'
            iam_client = self._get_client()
            response = await run_concurrently(
                    lambda: iam_client.projects().serviceAccounts().keys().list(name=name,
                                                                                keyTypes=key_types).execute()
            )
            return response.get('keys', [])
        except Exception as e:
            print_exception(f'Failed to retrieve service account keys: {e}')
            return []

    async def get_service_account_key(self, key_name: str):
        try:
            iam_client = self._get_client()
            response = await run_concurrently(
                lambda: iam_client.projects().serviceAccounts().keys().get(name=key_name,
                                                                           fields='').execute()
            )
            return response
        except Exception as e:
            print_exception(f'Failed to retrieve service account keys: {e}')
            return []

    async def get_role_definition(self, role: str):
        try:
            role = role.split("_withcond_")[0] # remove the condition key to get the actual role
            iam_client = self._get_client()
            if 'projects/' in role:
                response = await run_concurrently(
                    lambda: iam_client.projects().roles().get(name=role).execute()
                )
            elif 'organizations/' in role:
                response = await run_concurrently(
                    lambda: iam_client.organizations().roles().get(name=role).execute()
                )
            else:
                response = await run_concurrently(
                    lambda: iam_client.roles().get(name=role).execute()
                )
            return response
        except Exception as e:
            print_exception(f'Failed to retrieve IAM role definition for role {role}: {e}')
            return {}
