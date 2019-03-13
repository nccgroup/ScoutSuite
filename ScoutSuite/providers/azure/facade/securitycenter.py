from azure.mgmt.security import SecurityCenter
from ScoutSuite.providers.utils import run_concurrently


class SecurityCenterFacade:
    def __init__(self, credentials, subscription_id):
        self._client = SecurityCenter(credentials, subscription_id, '')

    async def get_pricings(self):
        return await run_concurrently(self._client.pricings.list)

    async def get_security_contacts(self):
        return await run_concurrently(self._client.security_contacts.list)

    async def get_auto_provisioning_settings(self):
        return await run_concurrently(self._client.auto_provisioning_settings.list)
