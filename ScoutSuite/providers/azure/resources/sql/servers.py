# -*- coding: utf-8 -*-

from azure.mgmt.sql import SqlManagementClient

from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.azure.utils import get_resource_group_name

from .databases import Databases
from .server_azure_ad_administrators import ServerAzureAdAdministrators
from ..utils import get_non_provider_id


class Servers(Resources):
    children = [
        Databases,
        ServerAzureAdAdministrators,
    ]

    async def fetch_all(self, credentials):
        # sdk container:
        api = SqlManagementClient(credentials.credentials, credentials.subscription_id)

        self['servers'] = {}
        # TODO: for server in await api.servers.list():
        for server in api.servers.list():
            id = get_non_provider_id(server.id)
            resource_group_name = get_resource_group_name(server.id)

            self['servers'][id] = {
                'id': id,
                'name': server.name
            }

            # put the following code in a fetch_children() parent method (typical method for a composite node)?
            for resources_class in self.children:
                resources = resources_class(resource_group_name, server.name)
                await resources.fetch_all(credentials)
                self['servers'][id].update(resources)
