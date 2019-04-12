from azure.mgmt.security import SecurityCenter
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.core.console import print_exception


class SecurityCenterFacade:
    def __init__(self, credentials, subscription_id):
        self._client = SecurityCenter(credentials, subscription_id, '')

    async def get_pricings(self):
        try:
            return await run_concurrently(
                lambda: list(self._client.pricings.list())
            )
        except Exception as e:
            print_exception('Failed to retrieve pricings: {}'.format(e))
            return []

    async def get_security_contacts(self):
        try:
            return await run_concurrently(
                lambda: list(self._client.security_contacts.list())
            )
        except Exception as e:
            print_exception('Failed to retrieve security contacts: {}'.format(e))
            return []

    async def get_auto_provisioning_settings(self):
        try:
            return await run_concurrently(
                lambda: list(self._client.auto_provisioning_settings.list())
            )
        except Exception as e:
            print_exception('Failed to retrieve auto provisioning settings: {}'.format(e))
            return []
