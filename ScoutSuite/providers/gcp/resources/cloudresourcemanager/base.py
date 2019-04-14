from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.cloudresourcemanager.bindings import Bindings


class CloudResourceManager(Projects):
    _children = [  
        (Bindings, 'bindings') 
    ]
