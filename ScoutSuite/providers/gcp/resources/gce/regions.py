from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.gcp.resources.projects import Projects

class ProjectRegions(Resources):
    def __init__(self, gcp_facade, project_id):
        self.gcp_facade = gcp_facade
        self.project_id = project_id

    async def fetch_all(self):
        raw_regions = await self.gcp_facade.gce.get_regions(self.project_id)
        for raw_region in raw_regions:
            region_name = raw_region['name']
            self[region_name] = {}


class Regions(Projects):
    async def fetch_all(self):
        super(Regions, self).fetch_all()
        for project_id in self['projects'].keys():
            project_regions = ProjectRegions(self.gcp_facade, project_id)
            await project_regions.fetch_all()
            self['projects'][project_id]['regions'] = project_regions
