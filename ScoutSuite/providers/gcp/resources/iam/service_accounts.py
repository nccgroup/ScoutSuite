# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.resources import CompositeResources
from ScoutSuite.providers.gcp.resources.iam.bindings import Bindings
from ScoutSuite.providers.gcp.resources.iam.keys import Keys

class ServiceAccounts(CompositeResources):
    _children = [
        ('bindings', Bindings),
        ('keys', Keys)
    ]

    def __init__(self, gcp_facade, project_id):
        self.gcp_facade = gcp_facade
        self.project_id = project_id

    async def fetch_all(self):
        raw_service_accounts = await self.gcp_facade.iam.get_service_accounts(self.project_id)
        for raw_service_account in raw_service_accounts:
            sa_id, service_account = self._parse_service_account(raw_service_account)
            self[sa_id] = service_account
        await self._fetch_children()
    
    async def _fetch_children(self):
        for sa_id, service_account in self.items():
            for child_name, child_class in self._children:
                child = child_class(self.iam_facade, self.project_id, service_account['email'])
                await child.fetch_all()
                self[sa_id][child_name] = child

    def _parse_service_account(self, raw_service_account):
        service_account_dict = {}
        service_account_dict['id'] = raw_service_account['uniqueId']
        service_account_dict['display_name'] = raw_service_account.get('displayName', 'N/A')
        service_account_dict['name'] = raw_service_account['name']
        service_account_dict['email'] = raw_service_account['email']
        service_account_dict['project_id'] = raw_service_account['projectId']
        return service_account_dict['id'], service_account_dict
