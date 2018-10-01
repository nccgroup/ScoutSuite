# -*- coding: utf-8 -*-

from ScoutSuite.providers.gcp.configs.base import GCPBaseConfig

from opinel.utils.console import printError, printException, printInfo


class CloudResourceManager(GCPBaseConfig):
    targets = (
        ('projects', 'Bindings', 'getIamPolicy', {'resource': 'project_placeholder'}, False),
    )

    def __init__(self, thread_config):

        self.library_type = 'api_client_library'

        self.bindings = {}
        self.bindings_count = 0

        super(CloudResourceManager, self).__init__(thread_config)

    # this is a misnammer, as the method returns IAM policies.
    # In addition, the 'project' method already exists for the BaseConfig object which creates a conflict.
    # TODO solve this is fhe Cloud Resource Manager needs to be used to get multiple things
    def parse_projects(self, binding, params):
        """
        """

        binding_dict = {}
        binding_dict['id'] = self.get_non_provider_id(binding['role'])
        binding_dict['name'] = binding['role'].split('/')[-1]
        binding_dict['members'] = binding['members']
        self.bindings[binding_dict['id']] = binding_dict

        # required as target is 'projects' and not 'bindings'
        self.bindings_count+=1
