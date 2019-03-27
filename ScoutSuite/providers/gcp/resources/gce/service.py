from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.gce.firewalls import Firewalls
from ScoutSuite.providers.gcp.resources.gce.instances import Instances
from ScoutSuite.providers.gcp.resources.gce.networks import Networks
from ScoutSuite.providers.gcp.resources.gce.snapshots import Snapshots
from ScoutSuite.providers.gcp.resources.gce.subnetworks import Subnetworks

class ComputeEngine(Projects):
    _children = [ 
        (Firewalls, 'firewalls'),
        (Instances, 'instances')
        (Networks, 'networks')
        (Snapshots, 'snapshots')
        (Subnetworks, 'subnetworks')
     ]

    def __init__(self, gcp_facade):
        super(ComputeEngine, self).__init__(gcp_facade)
