from ScoutSuite.providers.base.configs.base import BaseConfig

class GCPBaseConfig(BaseConfig):

    def __init__(self, thread_config=4, projects=None, **kwargs):
        self.projects = [] if projects is None else projects
        self.error_list = []  # list of errors, so that we don't print the same error multiple times
        super(GCPBaseConfig, self).__init__(thread_config)

    def _is_provider(self, provider_name):
        return provider_name == 'gcp'
