from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.utils import get_non_provider_id


class Bindings(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_bindings = await self.facade.cloudresourcemanager.get_member_bindings(self.project_id)
        for raw_binding in raw_bindings:
            binding_id, binding = await self._parse_binding(raw_binding)
            self[binding_id] = binding

    async def _parse_binding(self, raw_binding):
        binding_dict = {}
        binding_dict['id'] = get_non_provider_id(raw_binding['role'])
        binding_dict['name'] = raw_binding['role'].split('/')[-1]
        binding_dict['members'] = self._parse_members(raw_binding)
        binding_dict['custom_role'] = 'projects/' in raw_binding['role']

        role_definition = await self.facade.iam.get_role_definition(raw_binding['role'])

        binding_dict['title'] = role_definition.get('title')
        binding_dict['description'] = role_definition.get('description')
        binding_dict['permissions'] = role_definition.get('includedPermissions')

        return binding_dict['id'], binding_dict

    def _parse_members(self, raw_binding):
        members_dict = {'users': [], 'groups': [], 'service_accounts': [], 'domains': []}
        
        if 'members' not in raw_binding:
            return members_dict

        type_map = { 
            'user': 'users', 
            'group': 'groups', 
            'serviceAccount': 'service_accounts',
            'domain': 'domains'
        }
        
        # We want to group the members by type, so we need to parse their type and entity.
        # The members are given as strings with the format <member_type>:<member_entity>
        # See the GCP Resource Manager API reference for more info:
        # https://cloud.google.com/resource-manager/reference/rest/Shared.Types/Binding 
        for member in raw_binding['members']:
            member_type, entity = member.split(':')[:2]
            if member_type in type_map:
                members_dict[type_map[member_type]].append(entity)
            elif member_type == 'deleted':
                pass
            else:
                print_exception(f'Type {member_type} not handled')
        
        return members_dict
