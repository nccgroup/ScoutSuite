from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.cloudresourcemanager.bindings import Bindings
from ScoutSuite.providers.gcp.resources.cloudresourcemanager.users import Users
from ScoutSuite.providers.gcp.resources.cloudresourcemanager.groups import Groups


class CloudResourceManager(Projects):
    _children = [  
        (Bindings, 'bindings'),
        (Users, 'users'),
        (Groups, 'groups')
    ]
