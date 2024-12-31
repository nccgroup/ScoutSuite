from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.dns.managed_zones import ManagedZones
from ScoutSuite.providers.gcp.resources.dns.policies import Policies


class DNS(Projects):
    _children = [ 
        (ManagedZones, 'managed_zones'),
        (Policies, 'policies')
     ]
