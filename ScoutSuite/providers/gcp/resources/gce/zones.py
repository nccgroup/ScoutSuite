from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.gcp.resources.projects import Projects

class ProjectZones(Resources):
    def __init__(self, gcp_facade, project_id):
        self.gcp_facade = gcp_facade
        self.project_id = project_id

    async def fetch_all(self):
        raw_zones = await self.gcp_facade.gce.get_zones(self.project_id)
        for raw_zone in raw_zones:
            zone_name = raw_zone['name']
            self[zone_name] = {}


class Zones(Projects):
    async def fetch_all(self):
        super(Zones, self).fetch_all()
        for project_id in self['projects'].keys():
            project_zones = ProjectZones(self.gcp_facade, project_id)
            await project_zones.fetch_all()
            self['projects'][project_id]['zones'] = project_zones