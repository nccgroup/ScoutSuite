from ScoutSuite.providers.aws.resources.resources import AWSCompositeResources
from ScoutSuite.providers.utils import get_non_provider_id

from .cluster_parameters import ClusterParameters


class ClusterParameterGroups(AWSCompositeResources):
    _children = [
        (ClusterParameters, 'parameters')
    ]

    async def fetch_all(self, **kwargs):
        raw_parameter_groups = await self.facade.redshift.get_cluster_parameter_groups(self.scope['region'])
        # TODO: parallelize this async loop:
        for raw_parameter_group in raw_parameter_groups:
            id, parameter_group = self._parse_parameter_group(raw_parameter_group)
            await self._fetch_children(
                parent=parameter_group,
                scope={'region': self.scope['region'], 'parameter_group_name': parameter_group['name']}
            )
            self[id] = parameter_group

    def _parse_parameter_group(self, raw_parameter_group):
        name = raw_parameter_group.pop('ParameterGroupName')
        id = get_non_provider_id(name)
        raw_parameter_group['name'] = name

        return id, raw_parameter_group
