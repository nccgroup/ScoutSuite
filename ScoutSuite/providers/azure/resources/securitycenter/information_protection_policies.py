from ScoutSuite.providers.azure.resources.base import AzureResources


class InformationProtectionPolicies(AzureResources):
    async def fetch_all(self):
        for raw_information_policies in await self.facade.securitycenter.get_information_protection_policies():
            id, information_protection_policies = self._parse_information_protection_policies(
                raw_information_policies)
            self[id] = information_protection_policies

    def _parse_information_protection_policies(self, auto_provisioning_settings):
        information_protection_policies_dict = {}
        return information_protection_policies_dict['id'], information_protection_policies_dict
