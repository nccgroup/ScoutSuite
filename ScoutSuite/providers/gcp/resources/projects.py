import asyncio
from ScoutSuite.providers.gcp.facade.gcp import GCPFacade
from ScoutSuite.providers.gcp.resources.resources import GCPCompositeResources

class Projects(GCPCompositeResources):
    def __init__(self, gcp_facade: GCPFacade):
        self.gcp_facade = gcp_facade

    async def fetch_all(self, **kwargs):
        raw_projects = await self.gcp_facade.get_projects()
        self['projects'] = { raw_project['projectId'] : {} for raw_project in raw_projects }
        tasks = {
            asyncio.ensure_future(
                self._fetch_children(self['projects'][raw_project['projectId']], gcp_facade = self.gcp_facade, project_id = raw_project['projectId'])
            ) for raw_project in raw_projects
        }
        await asyncio.wait(tasks)
        self._set_counts()

    def _set_counts(self):
        for _, child_name in self._children:
            self[child_name + '_count'] = sum([project[child_name + '_count'] for project in self['projects'].values()])