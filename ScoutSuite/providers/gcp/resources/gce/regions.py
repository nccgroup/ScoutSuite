# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.gcp.resources.projects import Projects

class ProjectRegions(Resources):
    def __init__(self, gce_facade, project_id):
        self.gce_facade = gce_facade
        self.project_id = project_id

    def fetch_all(self):
        raw_regions = self.gce_facade.get_regions(self.project_id)
        for raw_region in raw_regions:
            region_name = raw_region['name']
            self[region_name] = {}


class Regions(Projects):
    def __init__(self, gcp_facade, gce_facade):
        super(Regions, self).__init__(gcp_facade)
        self.gce_facade = gce_facade

    def fetch_all(self):
        super(Regions, self).fetch_all()
        for project_id in self['projects'].keys():
            project_regions = ProjectRegions(self.gce_facade, project_id)
            project_regions.fetch_all()
            self['projects'][project_id]['regions'] = project_regions
