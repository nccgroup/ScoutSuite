# -*- coding: utf-8 -*-

from azure.mgmt.sql import SqlManagementClient

from ..resources import AzureCompositeResources
from ScoutSuite.providers.azure.utils import get_resource_group_name

from .databases import Databases
from .server_azure_ad_administrators import ServerAzureAdAdministrators
from ..utils import get_non_provider_id


class Servers(AzureCompositeResources):
    children = [
        Databases,
        ServerAzureAdAdministrators,
    ]

    # TODO: make it really async.
    async def fetch_all(self, credentials, **kwargs):
        # sdk container:
        api = SqlManagementClient(credentials.credentials, credentials.subscription_id)

        self['servers'] = {}
        for server in api.servers.list():
            id = get_non_provider_id(server.id)
            resource_group_name = get_resource_group_name(server.id)

            self['servers'][id] = {
                'id': id,
                'name': server.name
            }
            await self.fetch_children(
                parent=self['servers'][id],
                resource_group_name=resource_group_name,
                server_name=server.name,
                credentials=credentials)

        self['servers_count'] = len(self['servers'])
