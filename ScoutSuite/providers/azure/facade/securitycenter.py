from azure.mgmt.security import SecurityCenter

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently


class SecurityCenterFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        return SecurityCenter(self.credentials.arm_credentials, subscription_id, '')

    async def get_pricings(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: client.pricings.list().value
            )
        except Exception as e:
            print_exception('Failed to retrieve pricings: {}'.format(e))
            return []

    async def get_security_contacts(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.security_contacts.list())
            )
        except Exception as e:
            print_exception('Failed to retrieve security contacts: {}'.format(e))
            return []

    async def get_auto_provisioning_settings(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.auto_provisioning_settings.list())
            )
        except Exception as e:
            print_exception('Failed to retrieve auto provisioning settings: {}'.format(e))
            return []

    async def get_information_protection_policies(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            scope = '/subscriptions/{}'.format(self._subscription_id)
            return await run_concurrently(lambda: list(client.information_protection_policies.list(scope=scope)))
        except Exception as e:
            print_exception('Failed to retrieve information protection policies: {}'.format(e))
            return []

    async def get_settings(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.settings.list())
            )
        except Exception as e:
            print_exception('Failed to retrieve settings: {}'.format(e))
            return []
