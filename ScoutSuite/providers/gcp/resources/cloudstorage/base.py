from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.cloudstorage.buckets import Buckets


class CloudStorage(Projects):
    _children = [ 
        (Buckets, 'buckets')
    ]
