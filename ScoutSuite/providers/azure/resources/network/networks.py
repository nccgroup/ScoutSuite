from ScoutSuite.providers.azure.resources.resources import AzureCompositeResources
from ScoutSuite.providers.azure.facade.network import NetworkFacade

from .network_security_groups import NetworkSecurityGroups
from .network_watchers import NetworkWatchers


class Networks(AzureCompositeResources):
    _children = [
        (NetworkSecurityGroups, 'network_security_groups'),
        (NetworkWatchers, 'network_watchers')
    ]

    async def fetch_all(self, credentials, **kwargs):
        # TODO: build that facade somewhere else:
        facade = NetworkFacade(credentials.credentials, credentials.subscription_id)

        await self._fetch_children(parent=self, facade=facade)

        self['network_security_groups_count'] = len(self['network_security_groups'])
        self['network_watchers_count'] = len(self['network_watchers'])
