# -*- coding: utf-8 -*-

from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.cloudresourcemanager.bindings import Bindings

class CloudResourceManager(Projects):
    _children = [  
        ('bindings', Bindings) 
    ]

    def __init__(self, gcp_facade, resourcemanager_facade):
        super(CloudResourceManager, self).__init__(gcp_facade, resourcemanager_facade)

        
