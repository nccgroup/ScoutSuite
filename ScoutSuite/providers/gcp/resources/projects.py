import asyncio
from ScoutSuite.providers.gcp.facade.gcp import GCPFacade
from ScoutSuite.providers.gcp.resources.resources import GCPCompositeResources

class Projects(GCPCompositeResources):

    """This class represents a collection of GCP Resources that are grouped by project. 
    Classes extending Projects should implement the method _fetch_children() with a project ID as paramater.
    The children resources will be stored with the following structure {<projects>: {<project_id>: {<child_name>: {<child_id>: <child_instance>}}}}.
    """

    def __init__(self, gcp_facade: GCPFacade):
        self.gcp_facade = gcp_facade

    async def fetch_all(self, **kwargs):
        """This method fetches all the GCP projects that can be accessed with the given run configuration.
        It then fetches all the children defined in _children and groups them by project.
        """

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