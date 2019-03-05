from ScoutSuite.providers.azure.resources.resources import AzureCompositeResources
from ScoutSuite.providers.azure.utils import get_resource_group_name
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.providers.azure.facade.sqldatabase import SQLDatabaseFacade

from .databases import Databases
from .server_azure_ad_administrators import ServerAzureAdAdministrators


class Servers(AzureCompositeResources):
    _children = [
        Databases,
        ServerAzureAdAdministrators,
    ]

    # TODO: make it really async.
    async def fetch_all(self, credentials, **kwargs):
        # TODO: build that facade somewhere else:
        facade = SQLDatabaseFacade(credentials.credentials, credentials.subscription_id)

        self['servers'] = {}
        for server in await facade.get_servers():
            id = get_non_provider_id(server.id)
            resource_group_name = get_resource_group_name(server.id)

            self['servers'][id] = {
                'id': id,
                'name': server.name
            }
            await self._fetch_children(
                parent=self['servers'][id],
                resource_group_name=resource_group_name,
                server_name=server.name,
                facade=facade)

        self['servers_count'] = len(self['servers'])
