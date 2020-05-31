from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class RegulatoryComplianceResults(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super(RegulatoryComplianceResults, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_regulatory_compliance_result in await \
                self.facade.securitycenter.get_regulatory_compliance_results(self.subscription_id):
            id, regulatory_compliance_result = \
                self._parse_regulatory_compliance_result(raw_regulatory_compliance_result)
            self[id] = regulatory_compliance_result

    def _parse_regulatory_compliance_result(self, raw_regulatory_compliance_result):
        regulatory_compliance_result_dict = {}
        regulatory_compliance_result_dict['id'] = get_non_provider_id(raw_regulatory_compliance_result.id)
        regulatory_compliance_result_dict['name'] = '{} {}'.format(raw_regulatory_compliance_result.standard_name,
                                                                   raw_regulatory_compliance_result.name)
        regulatory_compliance_result_dict['reference'] = raw_regulatory_compliance_result.name
        regulatory_compliance_result_dict['standard_name'] = raw_regulatory_compliance_result.standard_name
        regulatory_compliance_result_dict['type'] = raw_regulatory_compliance_result.type
        regulatory_compliance_result_dict['description'] = raw_regulatory_compliance_result.description
        regulatory_compliance_result_dict['state'] = raw_regulatory_compliance_result.state
        regulatory_compliance_result_dict['passed_assessments'] = raw_regulatory_compliance_result.passed_assessments
        regulatory_compliance_result_dict['failed_assessments'] = raw_regulatory_compliance_result.failed_assessments
        regulatory_compliance_result_dict['skipped_assessments'] = raw_regulatory_compliance_result.skipped_assessments
        regulatory_compliance_result_dict['additional_properties'] = \
            raw_regulatory_compliance_result.additional_properties
        return regulatory_compliance_result_dict['id'], regulatory_compliance_result_dict
