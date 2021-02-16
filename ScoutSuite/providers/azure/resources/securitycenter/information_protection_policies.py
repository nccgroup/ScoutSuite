from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.core.console import print_exception


class InformationProtectionPolicies(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        parsing_error_counter = 0
        for raw_information_policies in await self.facade.securitycenter.get_information_protection_policies(
                self.subscription_id):
            try:
                id, information_protection_policies = self._parse_information_protection_policies(
                    raw_information_policies)
                self[id] = information_protection_policies
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_information_protection_policies(self, auto_provisioning_settings):
        information_protection_policies_dict = {}
        return information_protection_policies_dict['id'], information_protection_policies_dict
