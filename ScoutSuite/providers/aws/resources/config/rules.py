from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class Rules(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_rules = await self.facade.config.get_rules(self.region)
        parsing_error_counter = 0
        for raw_rule in raw_rules:
            try:
                name, resource = self._parse_rule(raw_rule)
                self[name] = resource
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_rule(self, raw_rule):
        rule = {}
        rule['id'] = raw_rule.pop('ConfigRuleId', None)
        rule['arn'] = raw_rule.pop('ConfigRuleArn', None)
        rule['name'] = raw_rule.pop('ConfigRuleName', None)
        rule['description'] = raw_rule.pop('Description', None)
        rule['scope'] = raw_rule.pop('Scope', None)
        rule['source'] = raw_rule.pop('Source', None)
        rule['input_parameters'] = raw_rule.pop('InputParameters', None)
        rule['maximum_execution_frequency'] = raw_rule.pop('MaximumExecutionFrequency', None)
        rule['state'] = raw_rule.pop('ConfigRuleState', None)
        return rule['name'], rule
