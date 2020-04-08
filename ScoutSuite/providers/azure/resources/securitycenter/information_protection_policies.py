from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class InformationProtectionPolicies(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super(InformationProtectionPolicies, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_information_policies in await self.facade.securitycenter.get_information_protection_policies(
                self.subscription_id):
            id, information_protection_policies = self._parse_information_protection_policies(
                raw_information_policies)
            self[id] = information_protection_policies

    def _parse_information_protection_policies(self, auto_provisioning_settings):
        information_protection_policies_dict = {}
        return information_protection_policies_dict['id'], information_protection_policies_dict
