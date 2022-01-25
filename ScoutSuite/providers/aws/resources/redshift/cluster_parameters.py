from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.utils import format_arn


class ClusterParameters(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, parameter_group_name: str):
        super().__init__(facade)
        self.region = region
        self.parameter_group_name = parameter_group_name
        self.partition = facade.partition
        self.service = 'redshift'
        self.resource_type = 'cluster-parameter'

    async def fetch_all(self):
        raw_parameters = await self.facade.redshift.get_cluster_parameters(
            self.region, self.parameter_group_name)
        for raw_parameter in raw_parameters:
            id, parameter = self._parse_parameter(raw_parameter)
            self[id] = parameter

    def _parse_parameter(self, raw_parameter):
        parameter = {'value': raw_parameter['ParameterValue'],
                     'source': raw_parameter['Source']}
        raw_parameter['arn'] = format_arn(self.partition, self.service, self.region, '', raw_parameter.get('ParameterName'), self.resource_type)
        return raw_parameter['ParameterName'], parameter
