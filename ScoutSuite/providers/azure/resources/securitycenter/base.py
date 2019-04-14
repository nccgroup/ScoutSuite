from ScoutSuite.providers.azure.resources.base import AzureCompositeResources

from .auto_provisioning_settings import AutoProvisioningSettings
from .pricings import Pricings
from .security_contacts import SecurityContacts


class SecurityCenter(AzureCompositeResources):
    _children = [
        (AutoProvisioningSettings, 'auto_provisioning_settings'),
        (Pricings, 'pricings'),
        (SecurityContacts, 'security_contacts')
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)
