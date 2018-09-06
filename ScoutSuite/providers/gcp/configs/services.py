# -*- coding: utf-8 -*-

from opinel.utils.console import printError, printException, printDebug

from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.providers.gcp.services.cloudstorage import CloudStorageConfig


class GCPServicesConfig(BaseServicesConfig):

    def __init__(self, metadata, thread_config=4):

        self.cloudstorage = CloudStorageConfig(thread_config)

    def _is_provider(self, provider_name):
        if provider_name == 'gcp':
            return True
        else:
            return False

