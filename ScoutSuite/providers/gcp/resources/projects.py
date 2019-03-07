# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.resources import CompositeResources

class Projects(CompositeResources):
    def __init__(self, gcp_facade, service_facade):
        self.gcp_facade = gcp_facade
        self.service_facade = service_facade

    async def fetch_all(self, **kwargs):
        raw_projects = self.gcp_facade.get_projects()
        self['projects'] = {}
        for raw_project in raw_projects:
            project_id = raw_project['projectId']
            self['projects'][project_id] = {}
        await self._fetch_children()

    async def _fetch_children(self):
        for project_id in self['projects'].keys():
            for child_name, child_class in self._children:
                child = child_class(self.service_facade, project_id)
                await child.fetch_all()
                self['projects'][project_id][child_name] = child
                self[child_name + '_count'] = len(child)