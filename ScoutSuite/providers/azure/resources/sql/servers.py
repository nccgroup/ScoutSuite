# -*- coding: utf-8 -*-

from azure.mgmt.sql import SqlManagementClient

from ScoutSuite.providers.base.configs.resource_config import ResourceConfig
from ScoutSuite.providers.azure.utils import get_resource_group_name

from .databases import DatabasesConfig
from .server_azure_ad_administrators import ServerAzureAdAdministratorsConfig
from ..utils import get_non_provider_id


class ServersConfig(ResourceConfig):
    # the following static methods will be used to parse the config of each resource nested in a server config
    # (defined in 'children' attribute below):
    @staticmethod
    def _parse_databases_config(config):
        return {
            'databases': config.databases
        }

    @staticmethod
    def _parse_azure_ad_administrators_config(config):
        return {
            'ad_admin_configured': config.value is not None
        }

    # register children resources:
    children = [
        (DatabasesConfig, _parse_databases_config),
        (ServerAzureAdAdministratorsConfig, _parse_azure_ad_administrators_config)
    ]

    def __init__(self):
        self.servers = {}

    async def fetch_all(self, credentials, regions=None, partition_name='aws', targets=None):
        # sdk container:
        api = SqlManagementClient(credentials.credentials, credentials.subscription_id)

        # for server in await api.servers.list():
        for server in api.servers.list():
            # parsing:

            id = get_non_provider_id(server.id)
            resource_group_name = get_resource_group_name(server.id)

            self.servers[id] = {
                'id': id,
                'name': server.name
            }

            # put the following code in a fetch_children() parent method (typical method for a composite node)?
            for (resource_config, resource_parser) in self.children:
                resource = resource_config(resource_group_name, server.name)
                await resource.fetch_all(credentials)
                for k, v in resource_parser.__func__(resource).items():
                    self.servers[id][k] = v
