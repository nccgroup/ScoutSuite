from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.gce.firewalls import Firewalls
from ScoutSuite.providers.gcp.resources.gce.networks import Networks
from ScoutSuite.providers.gcp.resources.gce.regions import Regions
from ScoutSuite.providers.gcp.resources.gce.snapshots import Snapshots
from ScoutSuite.providers.gcp.resources.gce.zones import Zones

class ComputeEngine(Projects):
    _children = [ 
        (Firewalls, 'firewalls'),
        (Networks, 'networks'),
        (Regions, 'regions'),
        (Snapshots, 'snapshots'),
        (Zones, 'zones'),
     ]

    async def fetch_all(self, **kwargs):
        await Projects.fetch_all(self, **kwargs)
        # Instances and Subnetworks are resources with 2 levels of filtering 
        # (project and region/zone), so we need to propagate their count up.
        # Normally this would be done by setting the resource counts in the Regions
        # and Zones classes, but having a "resource_name_count" field in their 
        # dictionary causes errors in the rule engine.
        instances_count = 0
        subnetworks_count = 0
        for project in self['projects'].values():
            for zone in project['zones'].values():
                instances_count += zone['instances_count']
            for region in project['regions'].values():
                subnetworks_count += region['subnetworks_count']
        self['instances_count'] = instances_count
        self['subnetworks_count'] = subnetworks_count
