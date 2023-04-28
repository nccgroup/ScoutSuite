from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.utils import get_non_provider_id


class KMSPolicy(Resources):

    def __init__(self, facade: GCPFacade, project_id: str, keyring_name: str, location: str, key_name: str):
        super().__init__(facade)
        self.project_id = project_id
        self.keyring_name = keyring_name
        self.location = location
        self.key_name = key_name

    async def fetch_all(self):
        raw_kms_bindings = await self.facade.kms.keys_iam_policy(self.project_id, self.location, self.keyring_name, self.key_name)
        for raw_kms_binding in raw_kms_bindings:
            kms_binding_id, kms_bindings = await self._parse_binding(raw_kms_binding)
            self[kms_binding_id] = kms_bindings

    async def _parse_binding(self, kms_raw_binding):
        kms_binding_dict = {}
        kms_binding_dict['id'] = get_non_provider_id(kms_raw_binding['role'])
        kms_binding_dict['name'] = kms_raw_binding['role'].split('/')[-1]
        kms_binding_dict['members'] = kms_raw_binding['members']
        kms_binding_dict['custom_role'] = 'projects/' in kms_raw_binding['role']
        kms_binding_dict['anonymous_public_accessible'] = self.keys_not_anonymous_public_accessible(kms_raw_binding)

        role_definition = await self.facade.iam.get_role_definition(kms_raw_binding['role'])

        kms_binding_dict['title'] = role_definition.get('title')
        kms_binding_dict['description'] = role_definition.get('description')
        kms_binding_dict['permissions'] = role_definition.get('includedPermissions')

        return kms_binding_dict['id'], kms_binding_dict

    def keys_not_anonymous_public_accessible(self, kms_raw_binding):
        if 'allUsers' in kms_raw_binding['members'] or 'allAuthenticatedUsers' in kms_raw_binding['members']:
            return False
        return True
