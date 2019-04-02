from ScoutSuite.providers.gcp.facade.gcp import GCPFacade
from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.cloudstorage.buckets import Buckets

class CloudStorage(Projects):
    _children = [ 
        (Buckets, 'buckets')
    ]

    def __init__(self, gcp_facade: GCPFacade):
        super(CloudStorage, self).__init__(gcp_facade)
