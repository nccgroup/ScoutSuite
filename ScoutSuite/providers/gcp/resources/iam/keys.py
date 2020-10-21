from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.core.console import print_exception


class Keys(Resources):
    def __init__(self, facade: GCPFacade, project_id: str, service_account_email: str):
        super().__init__(facade)
        self.project_id = project_id
        self.service_account_email = service_account_email 

    async def fetch_all(self):
        # fetch system managed keys
        raw_keys = await self.facade.iam.get_service_account_keys(self.project_id, self.service_account_email, ['SYSTEM_MANAGED'])
        for raw_key in raw_keys:
            try:
                key_id, key = await self._parse_key(raw_key, 'SYSTEM_MANAGED')
                self[key_id] = key
            except Exception as e:
                print_exception('Failed to parse {} resource: {}'.format(self.__class__.__name__, e))
        # fetch user managed keys
        raw_keys = await self.facade.iam.get_service_account_keys(self.project_id, self.service_account_email, ['USER_MANAGED'])
        for raw_key in raw_keys:
            try:
                key_id, key = await self._parse_key(raw_key, 'USER_MANAGED')
                self[key_id] = key
            except Exception as e:
                print_exception('Failed to parse {} resource: {}'.format(self.__class__.__name__, e))

    async def _parse_key(self, raw_key, key_type):
        key_dict = {}
        # The name of the key has the following format:
        # projects/{PROJECT_ID}/serviceAccounts/{ACCOUNT}/keys/{key}
        # https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts.keys
        key_dict['id'] = raw_key['name'].split('/')[-1]
        key_dict['valid_after'] = raw_key['validAfterTime']
        key_dict['valid_before'] = raw_key['validBeforeTime']
        key_dict['key_algorithm'] = raw_key['keyAlgorithm']
        key_dict['key_type'] = key_type

        return key_dict['id'], key_dict
