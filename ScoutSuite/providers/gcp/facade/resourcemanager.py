# -*- coding: utf-8 -*-

from googleapiclient import discovery
from ScoutSuite.providers.gcp.utils import MemoryCache

class ResourceManagerFacade:
    def __init__(self):
        self._resourcemanager_client = discovery.build('cloudresourcemanager', 'v1', cache_discovery=False, cache=MemoryCache())

    # TODO: Make truly async
    async def get_bindings(self, project_id):
        resource = f'projects/{project_id}'
        return self._resourcemanager_client.projects().getIamPolicy(resource=resource).execute()


