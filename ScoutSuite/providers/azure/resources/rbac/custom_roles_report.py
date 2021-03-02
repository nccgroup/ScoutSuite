from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class CustomRolesReport(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        custom_role_dict = {}
        custom_role_dict['id'] = self.subscription_id
        custom_role_dict['missing_custom_role_administering_resource_locks'] = True

        for raw_role in await self.facade.rbac.get_roles(self.subscription_id):
            if raw_role.role_name == 'Resource Lock Administrator':
                custom_role_dict['missing_custom_role_administering_resource_locks'] = False

        self[custom_role_dict['id']] = custom_role_dict


