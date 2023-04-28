from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.dns.managed_zones import ManagedZones


class DNS(Projects):
    _children = [ 
        (ManagedZones, 'managed_zones')
     ]
