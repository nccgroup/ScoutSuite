# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.services import BaseServicesConfig

from ScoutSuite.providers.gcp.services.cloudstorage import CloudStorageConfig

class GCPServicesConfig(BaseServicesConfig):

    def __init__(self, metadata, thread_config = 4):

        self.cloudstorage = CloudStorageConfig(metadata['storage']['cloudstorage'], thread_config)

    def fetch(self, credentials, services = [], regions = [], partition_name = ''):
        pass

    def postprocessing(self):
        pass


