from ScoutSuite.providers.openstack.resources.base import OpenstackResources


class Projects(OpenstackResources):
    async def fetch_all(self):
        raw_projects = await self.facade.keystone.get_projects()
        for raw_project in raw_projects:
            id, project = self._parse_project(raw_project)
            if id in self:
                continue

            self[id] = project

    def _parse_project(self, raw_project):
        project_dict = {}
        project_dict['id'] = raw_project.id
        project_dict['name'] = raw_project.name
        project_dict['domain_id'] = raw_project.domain_id
        project_dict['description'] = raw_project.description
        project_dict['enabled'] = raw_project.is_enabled
        project_dict['parent_id'] = raw_project.parent_id
        project_dict['is_domain'] = raw_project.is_domain
        project_dict['tags'] = raw_project.tags
        return project_dict['id'], project_dict
