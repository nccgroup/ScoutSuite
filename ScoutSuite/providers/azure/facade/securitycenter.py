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
            pricings_list = await run_concurrently(
                lambda: client.pricings.list()
            )
            if hasattr(pricings_list, 'value'):
                return pricings_list.value
            else:
                return []
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

    async def get_alerts(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.alerts.list())
            )
        except Exception as e:
            print_exception('Failed to retrieve alerts: {}'.format(e))
            return []

    async def get_compliance_results(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            scope = '/subscriptions/{}'.format(subscription_id)
            return await run_concurrently(
                lambda: list(client.compliance_results.list(scope=scope))
            )
        except Exception as e:
            print_exception('Failed to retrieve compliance results: {}'.format(e))
            return []

    async def get_regulatory_compliance_results(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            results = []
            try:
                compliance_standards = await run_concurrently(
                    lambda: list(client.regulatory_compliance_standards.list())
                )
            except Exception as e:
                print_exception('Failed to retrieve regulatory compliance standards: {}'.format(e))
                return {}
            else:
                for standard in compliance_standards:
                    try:
                        compliance_controls = await run_concurrently(
                            lambda: list(client.regulatory_compliance_controls.list(regulatory_compliance_standard_name=standard.name))
                        )
                        for control in compliance_controls:
                            control.standard_name = standard.name
                            results.append(control)
                    except Exception as e:
                        print_exception('Failed to retrieve compliance controls: {}'.format(e))
                        pass
            finally:
                return results
        except Exception as e:
            print_exception('Failed to retrieve regulatory compliance results: {}'.format(e))
            return []


