# -*- coding: utf-8 -*-

from opinel.utils.console import printError, printException, printInfo, printDebug

from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.providers.gcp.services.cloudstorage import CloudStorageConfig

class GCPServicesConfig(BaseServicesConfig):

    def __init__(self, metadata, thread_config = 4):

        self.cloudstorage = CloudStorageConfig(thread_config)

    def fetch(self, credentials, services = [], regions = [], partition_name = ''):
        for service in vars(self):
            try:
                # skip services
                if services != [] and service not in services:
                    continue
                service_config = getattr(self, service)
                # call fetch method for the service
                if 'fetch_all' in dir(service_config):
                    method_args = {}
                    method_args['credentials'] = credentials
                    method_args['regions'] = regions
                    service_config.fetch_all(**method_args)
                    if hasattr(service_config, 'finalize'):
                        service_config.finalize()
                else:
                    printDebug('No method to fetch service %s.' % service)
            except Exception as e:
                printError('Error: could not fetch %s configuration.' % service)
                printException(e)

    def postprocessing(self):
        pass


