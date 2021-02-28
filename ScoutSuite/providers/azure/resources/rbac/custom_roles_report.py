from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class CustomRolesReport(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_role in await self.facade.rbac.get_roles(self.subscription_id):
            self._parse_role(raw_role)

    def _parse_role(self, raw_role):
        self['missing_custom_role_administering_resource_locks'] = True
