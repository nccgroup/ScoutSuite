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
