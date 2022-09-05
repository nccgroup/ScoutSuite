from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.basefacade import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils
from ScoutSuite.providers.utils import run_concurrently

class CloudSQLFacade(GCPBaseFacade):
    def __init__(self):
        super().__init__('sqladmin', 'v1beta4')

    async def get_backups(self, project_id: str, instance_name: str):
        try:
            cloudsql_client = self._get_client()
            backups_group = cloudsql_client.backupRuns()
            request = backups_group.list(project=project_id, instance=instance_name)
            return await GCPFacadeUtils.get_all('items', request, backups_group)
        except Exception as e:
            print_exception(f'Failed to retrieve database instance backups: {e}')
            return []

    async def get_database_instances(self, project_id: str):
        try:
            cloudsql_client = self._get_client()
            instances_group = cloudsql_client.instances()
            request = instances_group.list(project=project_id)
            return await GCPFacadeUtils.get_all('items', request, instances_group)
        except Exception as e:
            print_exception(f'Failed to retrieve database instances: {e}')
            return []

    async def get_users(self, project_id: str, instance_name: str):
        try:
            cloudsql_client = self._get_client()
            response = await run_concurrently(
                    lambda: cloudsql_client.users().list(project=project_id, instance=instance_name).execute()
            )
            return response.get('items', [])
        except Exception as e:
            if 'The requested operation is not valid for an on-premises instance.' in str(e):
                return []
            if 'Invalid request since instance is not running' not in str(e):
                print_exception(f'Failed to retrieve database instance users: {e}')
            return []
