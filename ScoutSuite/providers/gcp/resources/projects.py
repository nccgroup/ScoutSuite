from ScoutSuite.providers.gcp.resources.base import GCPCompositeResources


class Projects(GCPCompositeResources):

    """This class represents a collection of GCP Resources that are grouped by project. 
    Classes extending Projects should implement the method _fetch_children() with a project ID as paramater.
    The children resources will be stored with the following structure {<projects>: {<project_id>: {<child_name>: {<child_id>: <child_instance>}}}}.
    """

    async def fetch_all(self):
        """This method fetches all the GCP projects that can be accessed with the given run configuration.
        It then fetches all the children defined in _children and groups them by project.
        """

        raw_projects = await self.facade.get_projects()

        self['projects'] = {}
        # For each project, validate that the corresponding service API is enabled before including it in the execution.
        for p in raw_projects:
            enabled = await self.facade.is_api_enabled(p['projectId'], self.__class__.__name__)
            if enabled:
                self['projects'][p['projectId']] = {}

        await self._fetch_children_of_all_resources(
            resources=self['projects'],
            scopes={project_id: {'project_id': project_id} for project_id in self['projects']})
        self._set_counts()

    def _set_counts(self):
        for _, child_name in self._children:
            self[child_name + '_count'] = sum([project[child_name + '_count']
                                               for project in self['projects'].values()])
