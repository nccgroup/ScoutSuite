# -*- coding: utf-8 -*-

from opinel.utils.console import printError, printException, printDebug

from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.providers.gcp.services.cloudstorage import CloudStorageConfig
from ScoutSuite.providers.gcp.services.cloudsql import CloudSQLConfig
from ScoutSuite.providers.gcp.services.iam import IAMConfig
from ScoutSuite.providers.gcp.services.stackdriverlogging import StackdriverLoggingConfig
from ScoutSuite.providers.gcp.services.stackdrivermonitoring import StackdriverMonitoringConfig
from ScoutSuite.providers.gcp.services.computeengine import ComputeEngineConfig
from ScoutSuite.providers.gcp.services.cloudresourcemanager import CloudResourceManager

try:
    from ScoutSuite.providers.gcp.services.kubernetesengine_private import KubernetesEngineConfig
except ImportError:
    pass


class GCPServicesConfig(BaseServicesConfig):

    def __init__(self, metadata=None, thread_config=4, projects=None, **kwargs):

        projects = [] if projects is None else projects

        self.cloudresourcemanager = CloudResourceManager(thread_config=thread_config)
        self.cloudstorage = CloudStorageConfig(thread_config=thread_config)
        self.cloudsql = CloudSQLConfig(thread_config=thread_config)
        self.computeengine = ComputeEngineConfig(thread_config=thread_config)
        self.iam = IAMConfig(thread_config=thread_config)

        try:
            self.kubernetesengine = KubernetesEngineConfig(thread_config=thread_config)
        except NameError as e:
            pass

        self.stackdriverlogging = StackdriverLoggingConfig(thread_config=thread_config)
        # self.stackdrivermonitoring = StackdriverMonitoringConfig(thread_config=thread_config)

    def _is_provider(self, provider_name):
        return provider_name == 'gcp'

    def set_projects(self, projects):
        """
        Set the projects attribute of each of the configs. This is because before authentication (when configs
        are instanciated, the projects within an organization are not known).

        :param projects: List of projects to set
        :return: None
        """

        for c in vars(self):
            setattr(getattr(self, c), 'projects', projects)

