from ScoutSuite.providers.aws.resources.resources import AWSResources


class ClusterParameters(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_parameters = await self.facade.redshift.get_cluster_parameters(
            self.scope['region'], self.scope['parameter_group_name'])
        for raw_parameter in raw_parameters:
            id, parameter = self._parse_parameter(raw_parameter)
            self[id] = parameter

    def _parse_parameter(self, raw_parameter):
        parameter = {'value': raw_parameter['ParameterValue'],
                     'source': raw_parameter['Source']}
        return raw_parameter['ParameterName'], parameter
