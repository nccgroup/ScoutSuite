# -*- coding: utf-8 -*-

from ScoutSuite.providers.gcp.configs.base import GCPBaseConfig

from opinel.utils.console import printError, printException, printInfo


class CloudResourceManager(GCPBaseConfig):
    targets = (
        ('projects', 'Bindings', 'getIamPolicy', {'resource': '{{project_placeholder}}'}, False),
    )

    def __init__(self, thread_config):

        self.library_type = 'api_client_library'

        self.bindings = {}
        self.bindings_count = 0

        super(CloudResourceManager, self).__init__(thread_config)

    # this is a misnamer, as the method returns IAM policies.
    # In addition, the 'project' method already exists for the BaseConfig object which creates a conflict.
    # TODO solve this if the Cloud Resource Manager needs to be used to get multiple things
    def parse_projects(self, binding, params):
        """
        """

        binding_dict = {}
        binding_dict['id'] = self.get_non_provider_id(binding['role'])
        binding_dict['name'] = binding['role'].split('/')[-1]

        binding_dict['members'] = {'users': [],
                                   'groups': [],
                                   'service_accounts': []}
        if 'members' in binding:
            for member in binding['members']:
                type = member.split(':')[0]
                entity = member.split(':')[1]
                if type == 'user':
                    binding_dict['members']['users'].append(entity)
                elif type == 'group':
                    binding_dict['members']['groups'].append(entity)
                elif type == 'serviceAccount':
                    binding_dict['members']['service_accounts'].append(entity)
                else:
                    printException('Type %s not handled' % type)

        self.bindings[binding_dict['id']] = binding_dict

        # required as target is 'projects' and not 'bindings'
        self.bindings_count+=1
