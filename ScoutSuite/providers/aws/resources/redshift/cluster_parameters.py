from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class ClusterParameters(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, parameter_group_name: str):
        super().__init__(facade)
        self.region = region
        self.parameter_group_name = parameter_group_name

    async def fetch_all(self):
        raw_parameters = await self.facade.redshift.get_cluster_parameters(
            self.region, self.parameter_group_name)
        parsing_error_counter = 0
        for raw_parameter in raw_parameters:
            try:
                id, parameter = self._parse_parameter(raw_parameter)
                self[id] = parameter
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_parameter(self, raw_parameter):
        parameter = {'value': raw_parameter['ParameterValue'],
                     'source': raw_parameter['Source']}
        return raw_parameter['ParameterName'], parameter
