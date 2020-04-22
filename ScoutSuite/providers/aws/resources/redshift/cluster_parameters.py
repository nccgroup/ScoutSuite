from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class ClusterParameters(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, parameter_group_name: str):
        super(ClusterParameters, self).__init__(facade)
        self.region = region
        self.parameter_group_name = parameter_group_name

    async def fetch_all(self):
        raw_parameters = await self.facade.redshift.get_cluster_parameters(
            self.region, self.parameter_group_name)
        for raw_parameter in raw_parameters:
            id, parameter = self._parse_parameter(raw_parameter)
            self[id] = parameter

    def _parse_parameter(self, raw_parameter):
        parameter = {'value': raw_parameter['ParameterValue'],
                     'source': raw_parameter['Source']}
        return raw_parameter['ParameterName'], parameter
