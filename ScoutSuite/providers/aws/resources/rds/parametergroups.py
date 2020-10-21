from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.core.console import print_exception


class ParameterGroups(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_parameter_groups = await self.facade.rds.get_parameter_groups(self.region)
        for raw_parameter_group in raw_parameter_groups:
            try:
                name, resource = self._parse_parameter_group(raw_parameter_group)
                self[name] = resource
            except Exception as e:
                print_exception('Failed to parse {} resource: {}'.format(self.__class__.__name__, e))

    def _parse_parameter_group(self, raw_parameter_group):
        raw_parameter_group['arn'] = raw_parameter_group.pop('DBParameterGroupArn')
        raw_parameter_group['name'] = raw_parameter_group.pop('DBParameterGroupName')
        raw_parameter_group['parameters'] = raw_parameter_group.pop('Parameters')
        parameter_group_id = get_non_provider_id(raw_parameter_group['name'])
        return parameter_group_id, raw_parameter_group
