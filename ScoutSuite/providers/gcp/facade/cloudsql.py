# -*- coding: utf-8 -*-

from googleapiclient import discovery
from ScoutSuite.providers.gcp.utils import MemoryCache

class CloudSQLFacade:
    def __init__(self):
        self._cloudsql_client = discovery.build('sqladmin', 'v1beta4', cache_discovery=False, cache=MemoryCache())

    # TODO: Make truly async
    async def get_backups(self, project_id, instance_name):
        backups = []
        request = self._cloudsql_client.backupRuns().list(project=project_id, instance=instance_name)
        while request is not None:
            response = request.execute()
            backups.extend(response.get('items', []))
            request = self._cloudsql_client.backupRuns().list_next(previous_request=request, previous_response=response)
        return backups

    # TODO: Make truly async
    async def get_database_instances(self, project_id):
        database_instances = []
        request = self._cloudsql_client.instances().list(project=project_id)
        while request is not None:
            response = request.execute()
            database_instances.extend(response.get('items', []))
            request = self._cloudsql_client.instances().list_next(previous_request=request, previous_response=response)
        return database_instances

    # TODO: Make truly async
    async def get_users(self, project_id, instance_name):
        users = self._cloudsql_client.users().list(project=project_id, instance=instance_name).execute()
        return users.get('items', [])