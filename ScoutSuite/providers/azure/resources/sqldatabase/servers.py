import asyncio

from ScoutSuite.providers.azure.resources.resources import AzureCompositeResources
from ScoutSuite.providers.azure.utils import get_resource_group_name
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.providers.azure.facade.sqldatabase import SQLDatabaseFacade

from .databases import Databases
from .server_azure_ad_administrators import ServerAzureAdAdministrators
from .server_blob_auditing_policies import ServerBlobAuditingPolicies
from .server_security_alert_policies import ServerSecurityAlertPolicies


class Servers(AzureCompositeResources):
    _children = [
        (Databases, 'databases'),
        (ServerAzureAdAdministrators, None),
        (ServerBlobAuditingPolicies, 'auditing'),
        (ServerSecurityAlertPolicies, 'threat_detection')
    ]

    async def fetch_all(self, credentials, **kwargs):
        self['servers'] = {}
        for server in await self.facade.sqldatabase.get_servers():
            id = get_non_provider_id(server.id)
            resource_group_name = get_resource_group_name(server.id)

            self['servers'][id] = {
                'id': id,
                'name': server.name,
                'resource_group_name': resource_group_name
            }

        # TODO: make a refactoring of the following:
        if len(self['servers']) == 0:
            return
        tasks = {
            asyncio.ensure_future(
                self._fetch_children(
                    parent=server,
                    resource_group_name=server['resource_group_name'],
                    server_name=server['name'],
                    facade=self.facade
                )
            ) for server in self['servers'].values()
        }
        await asyncio.wait(tasks)

        self['servers_count'] = len(self['servers'])
