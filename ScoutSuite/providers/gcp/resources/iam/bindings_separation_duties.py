from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade


class BindingsSeparationDuties(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_bindings = await self.facade.cloudresourcemanager.get_member_bindings(self.project_id)
        binding_id, binding = await self._parse_binding_separation(raw_bindings)
        self[binding_id] = binding

    async def _parse_binding_separation(self, raw_bindings):
        binding_dict = {}
        binding_dict['id'] = self.project_id
        binding_dict['name'] = self.project_id
        binding_dict["account_separation_duties"] = self.ensure_seperation_duties(raw_bindings)
        binding_dict["kms_separation_duties"] = self.ensure_KMS_seperation_duties(raw_bindings)

        return binding_dict['id'], binding_dict

    def ensure_seperation_duties(self, raw_bindings):
        # This function checks if a member has both the iam.serviceAccountAdmin role and iam.serviceAccountUser role.
        # If the roles do have a common member the function returns False
        list_members_role_admin = []
        list_members_role_other = []
        for binding in raw_bindings:
            role = binding['role'].split('/')[-1]
            if role == 'iam.serviceAccountAdmin':
                list_members_role_admin = binding['members']
            if role == 'iam.serviceAccountUser':
                list_members_role_other = binding['members']

        common_members = list(set(list_members_role_admin).intersection(list_members_role_other))
        if common_members:
            return False
        return True

    def ensure_KMS_seperation_duties(self, raw_bindings):
        # This function checks if a member has both the cloudkms.admin role and either
        # cloudkms.cryptoKeyEncrypterDecrypter, cloudkms.cryptoKeyEncrypter, cloudkms.cryptoKeyDecrypter role.
        # If the roles do have a common member the function returns False
        list_members_role_admin = []
        list_members_role_others = {"cloudkms.cryptoKeyEncrypterDecrypter": [],
                                    "cloudkms.cryptoKeyEncrypter": [],
                                    "cloudkms.cryptoKeyDecrypter": []}
        for binding in raw_bindings:
            role = binding['role'].split('/')[-1]
            if role == 'cloudkms.admin':
                list_members_role_admin = binding['members']
            if role == 'cloudkms.cryptoKeyEncrypterDecrypter':
                list_members_role_others['cloudkms.cryptoKeyEncrypterDecrypter'] = binding['members']
            if role == 'cloudkms.cryptoKeyEncrypter':
                list_members_role_others['cloudkms.cryptoKeyEncrypter'] = binding['members']
            if role == 'cloudkms.cryptoKeyDecrypter':
                list_members_role_others['cloudkms.cryptoKeyDecrypter'] = binding['members']

        common_members1 = list(
            set(list_members_role_admin).intersection(list_members_role_others['cloudkms.cryptoKeyEncrypterDecrypter']))
        common_members2 = list(
            set(list_members_role_admin).intersection(list_members_role_others['cloudkms.cryptoKeyEncrypter']))
        common_members3 = list(
            set(list_members_role_admin).intersection(list_members_role_others['cloudkms.cryptoKeyDecrypter']))
        if common_members1 or common_members2 or common_members3:
            return False
        return True
