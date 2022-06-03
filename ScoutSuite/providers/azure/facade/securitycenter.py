from azure.mgmt.security import SecurityCenter

from ScoutSuite.core.console import print_exception, print_debug
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.utils import get_user_agent


class SecurityCenterFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        client = SecurityCenter(self.credentials.get_credentials(),
                                subscription_id, '',
                                user_agent=get_user_agent())
        return client

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
            print_exception(f'Failed to retrieve pricings: {e}')
            return []

    async def get_security_contacts(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.security_contacts.list())
            )
        except Exception as e:
            print_exception(f'Failed to retrieve security contacts: {e}')
            return []

    async def get_auto_provisioning_settings(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.auto_provisioning_settings.list())
            )
        except Exception as e:
            print_exception(f'Failed to retrieve auto provisioning settings: {e}')
            return []

    async def get_information_protection_policies(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            scope = f'/subscriptions/{self._subscription_id}'
            return await run_concurrently(lambda: list(client.information_protection_policies.list(scope=scope)))
        except Exception as e:
            print_exception(f'Failed to retrieve information protection policies: {e}')
            return []

    async def get_settings(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.settings.list())
            )
        except Exception as e:
            print_exception(f'Failed to retrieve settings: {e}')
            return []

    async def get_alerts(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.alerts.list())
            )
        except Exception as e:
            print_exception(f'Failed to retrieve alerts: {e}')
            return []

    def remove_last_ItemPage_from_the_list(self, results):
        p = list()
        try:
            for i in results:
                p.append(i)
        except Exception:
        # TODO implement condition to pass only if the triggered error is MissingApiVersionParameter
            pass
        return p
    
    """
    Commented out this part since a weird bug causes MissingApiVersionParameter errors to appear in the last response from Azure API. 
    Workaround bypasses this but obviously not ideal.
    
    async def get_compliance_results(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            scope = f'/subscriptions/{subscription_id}'
            return await run_concurrently(
                lambda: list(client.compliance_results.list(scope=scope))
            )
        except Exception as e:
            print_exception(f'Failed to retrieve compliance results: {e}')
            return []
     """
            
    async def get_compliance_results(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            scope = f'/subscriptions/{subscription_id}'
            return await run_concurrently(
                lambda: self.remove_last_ItemPage_from_the_list(client.compliance_results.list(scope=scope))
            )
        except Exception as e:
            print_exception(f'Failed to retrieve compliance results: {e}')
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
                if 'as it has no standard pricing bundle' in str(e):
                    print_debug(f'Failed to retrieve regulatory compliance standards: {e}')
                else:
                    print_exception(f'Failed to retrieve regulatory compliance standards: {e}')
                return {}
            else:
                for standard in compliance_standards:
                    try:
                        compliance_controls = await run_concurrently(
                            lambda standard=standard: list(client.regulatory_compliance_controls.list(
                                regulatory_compliance_standard_name=standard.name))
                        )
                        for control in compliance_controls:
                            control.standard_name = standard.name
                            results.append(control)
                    except Exception as e:
                        print_exception(f'Failed to retrieve compliance controls: {e}')
            finally:
                return results
        except Exception as e:
            print_exception(f'Failed to retrieve regulatory compliance results: {e}')
            return []
