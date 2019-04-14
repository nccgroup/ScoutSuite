from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.gce.firewalls import Firewalls
from ScoutSuite.providers.gcp.resources.gce.networks import Networks
from ScoutSuite.providers.gcp.resources.gce.regions import GCERegions
from ScoutSuite.providers.gcp.resources.gce.snapshots import Snapshots
from ScoutSuite.providers.gcp.resources.gce.zones import GCEZones


class ComputeEngine(Projects):
    _children = [ 
        (Firewalls, 'firewalls'),
        (Networks, 'networks'),
        (GCERegions, 'regions'),
        (Snapshots, 'snapshots'),
        (GCEZones, 'zones'),
     ]

    async def fetch_all(self):
        await Projects.fetch_all(self)
        # Instances and Subnetworks are resources with 2 levels of filtering 
        # (project and region/zone), so we need to propagate their count up.
        # Normally this would be done by setting the resource counts in the Regions
        # and Zones classes, but having a "resource_name_count" field in their 
        # dictionary causes errors in the rule engine.
        self['instances_count'] = sum(sum(
            zone['instances_count'] for zone in project['zones'].values()) for project in self['projects'].values())
        self['subnetworks_count'] = sum(sum(
            region['subnetworks_count'] for region in project['regions'].values())
                                        for project in self['projects'].values())
        del self['regions_count']
        del self['zones_count']
