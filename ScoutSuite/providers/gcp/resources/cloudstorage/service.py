# -*- coding: utf-8 -*-

from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.cloudstorage.buckets import Buckets

class CloudStorage(Projects):
    _children = [ 
        ('buckets', Buckets)
    ]

    def __init__(self, gcp_facade, cloudstorage_facade):
        super(CloudStorage, self).__init__(gcp_facade, cloudstorage_facade)
