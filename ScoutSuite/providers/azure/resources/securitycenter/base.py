from ScoutSuite.providers.azure.resources.base import AzureCompositeResources

from .auto_provisioning_settings import AutoProvisioningSettings
from .pricings import Pricings
from .security_contacts import SecurityContacts
# from .information_protection_policies import InformationProtectionPolicies
# from .settings import Settings


class SecurityCenter(AzureCompositeResources):
    _children = [
        (AutoProvisioningSettings, 'auto_provisioning_settings'),
        (Pricings, 'pricings'),
        (SecurityContacts, 'security_contacts'),
        # (InformationProtectionPolicies, 'information_protection_policies'),  # FIXME this isn't properly implemented
        # (Settings, 'settings')  # FIXME this isn't implemented
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)
