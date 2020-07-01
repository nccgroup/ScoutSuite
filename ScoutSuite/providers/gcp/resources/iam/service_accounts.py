from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.gcp.resources.base import GCPCompositeResources
from ScoutSuite.providers.gcp.resources.iam.service_account_bindings import ServiceAccountBindings
from ScoutSuite.providers.gcp.resources.iam.keys import Keys
import re


class ServiceAccounts(GCPCompositeResources):
    _children = [
        (ServiceAccountBindings, 'bindings'),
        (Keys, 'keys')
    ]

    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_service_accounts = await self.facade.iam.get_service_accounts(self.project_id)
        for raw_service_account in raw_service_accounts:
            service_account_id, service_account = self._parse_service_account(
                raw_service_account)
            self[service_account_id] = service_account
            await self._fetch_children(
                self[service_account_id],
                scope={'project_id': self.project_id, 'service_account_email': service_account['email']})

    def _parse_service_account(self, raw_service_account):
        service_account_dict = {}
        service_account_dict['id'] = raw_service_account['uniqueId']
        service_account_dict['display_name'] = raw_service_account.get(
            'displayName', 'N/A')
        service_account_dict['name'] = raw_service_account['email']
        service_account_dict['email'] = raw_service_account['email']
        service_account_dict['project_id'] = raw_service_account['projectId']

        pattern = re.compile(r'.+@{}\.iam\.gserviceaccount\.com'.format(service_account_dict['project_id']))
        if pattern.match(service_account_dict['email']):
            service_account_dict['default_service_account'] = False
        else:
            service_account_dict['default_service_account'] = True

        return service_account_dict['id'], service_account_dict
