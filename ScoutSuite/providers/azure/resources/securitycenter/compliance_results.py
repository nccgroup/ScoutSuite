from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.core.console import print_exception


class ComplianceResults(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        parsing_error_counter = 0
        for raw_compliance_result in await self.facade.securitycenter.get_compliance_results(self.subscription_id):
            try:
                id, compliance_result = self._parse_compliance_result(raw_compliance_result)
                self[id] = compliance_result
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_compliance_result(self, raw_compliance_result):
        compliance_result_dict = {}
        compliance_result_dict['id'] = get_non_provider_id(raw_compliance_result.id)
        compliance_result_dict['name'] = raw_compliance_result.name
        compliance_result_dict['type'] = raw_compliance_result.type
        compliance_result_dict['resource_status'] = raw_compliance_result.resource_status
        compliance_result_dict['additional_properties'] = raw_compliance_result.additional_properties
        return compliance_result_dict['id'], compliance_result_dict
