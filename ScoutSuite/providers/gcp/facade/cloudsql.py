from ScoutSuite.providers.gcp.facade.facade import Facade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils
from ScoutSuite.providers.utils import run_concurrently

class CloudSQLFacade(Facade):
    def __init__(self):
        super(CloudSQLFacade, self).__init__('sqladmin', 'v1beta4')

    async def get_backups(self, project_id, instance_name):
        cloudsql_client = self._get_client()
        backups_group = cloudsql_client.backupRuns()
        request = backups_group.list(project=project_id, instance=instance_name)
        return await GCPFacadeUtils.get_all('items', request, backups_group)

    async def get_database_instances(self, project_id):
        cloudsql_client = self._get_client()
        instances_group = cloudsql_client.instances()
        request = instances_group.list(project=project_id)
        return await GCPFacadeUtils.get_all('items', request, instances_group)

    async def get_users(self, project_id, instance_name):
        cloudsql_client = self._get_client()
        response = await run_concurrently(
                lambda: cloudsql_client.users().list(project=project_id, instance=instance_name).execute()
        )
        return response.get('items', [])
        