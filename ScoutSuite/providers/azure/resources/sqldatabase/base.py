from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.utils import get_resource_group_name
from ScoutSuite.providers.utils import get_non_provider_id

from .databases import Databases
from .server_azure_ad_administrators import ServerAzureAdAdministrators
from .server_blob_auditing_policies import ServerBlobAuditingPolicies
from .server_security_alert_policies import ServerSecurityAlertPolicies


class Servers(Subscriptions):

    _children = [
        (Databases, 'databases'),
        (ServerAzureAdAdministrators, None),
        (ServerBlobAuditingPolicies, 'auditing'),
        (ServerSecurityAlertPolicies, 'threat_detection')
    ]

    # def __init__(self, facade: AzureFacade, subscription_id: str):
    #     super(Servers, self).__init__(facade)
    #     self.subscription_id = subscription_id

    async def fetch_all(self):
        # TODO servers should be a resource in a separate file
        self['servers'] = {}
        for server in await self.facade.sqldatabase.get_servers():
            id = get_non_provider_id(server.id)
            resource_group_name = get_resource_group_name(server.id)

            self['servers'][id] = {
                'id': id,
                'name': server.name,
                'resource_group_name': resource_group_name
            }
        self['servers_count'] = len(self['servers'])

        await self._fetch_children_of_all_resources(
            resources=self['servers'],
            scopes={server_id: {'resource_group_name': server['resource_group_name'],
                                'server_name': server['name']}
                    for (server_id, server) in self['servers'].items()}
        )
