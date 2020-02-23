from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from ScoutSuite.providers.utils import get_non_provider_id

from .cluster_parameters import ClusterParameters


class ClusterParameterGroups(AWSCompositeResources):
    _children = [
        (ClusterParameters, 'parameters')
    ]

    def __init__(self, facade: AWSFacade, region: str):
        super(ClusterParameterGroups, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_parameter_groups = await self.facade.redshift.get_cluster_parameter_groups(self.region)
        for raw_parameter_group in raw_parameter_groups:
            id, parameter_group = self._parse_parameter_group(raw_parameter_group)
            self[id] = parameter_group

        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={parameter_group_id: {'region': self.region,
                                         'parameter_group_name': parameter_group['name']}
                    for (parameter_group_id, parameter_group) in self.items()}
        )

    def _parse_parameter_group(self, raw_parameter_group):
        parameter_group = {}
        parameter_group['name'] = raw_parameter_group.get('ParameterGroupName')
        parameter_group['id'] = get_non_provider_id(parameter_group['name'])
        parameter_group['family'] = raw_parameter_group.get('ParameterGroupFamily')
        parameter_group['description'] = raw_parameter_group.get('Description')
        parameter_group['is_default'] = self._is_default(raw_parameter_group)
        parameter_group['tags'] = raw_parameter_group.get('Tags')
        return parameter_group['id'], parameter_group

    def _is_default(self, raw_parameter_group):
        if 'Default parameter group for' in raw_parameter_group.get('Description') and \
                'default.' in raw_parameter_group.get('ParameterGroupName'):
            return True
        else:
            return False
