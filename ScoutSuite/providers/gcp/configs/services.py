# -*- coding: utf-8 -*-

from opinel.utils.console import printError, printException, printDebug

from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.providers.gcp.services.cloudstorage import CloudStorageConfig
from ScoutSuite.providers.gcp.services.cloudsql import CloudSQLConfig



class GCPServicesConfig(BaseServicesConfig):

    def __init__(self, metadata=None, thread_config=4, projects=[], **kwargs):

        self.cloudstorage = CloudStorageConfig(thread_config=thread_config)
        self.cloudsql = CloudSQLConfig(thread_config=thread_config)

    def _is_provider(self, provider_name):
        if provider_name == 'gcp':
            return True
        else:
            return False

    def set_projects(self, projects):
        self.cloudstorage.projects = projects
        self.cloudsql.projects = projects


