from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions
from ScoutSuite.providers.aws.resources.base import AWSResources


class RecorderStatus(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(RecorderStatus, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_recorder_status_list = await self.facade.config.get_recorder_status(self.region)
        for raw_recorder_status in raw_recorder_status_list:
            name, resource = self._parse_recorder_status(raw_recorder_status)
            self[name] = resource

    def _parse_recorder_status(self, raw_recorder_status):
        # Drop some data
        for key in ['lastStartTime', 'lastStatus', 'lastStatusChangeTime']:
            if key in raw_recorder_status:
                raw_recorder_status.pop(key)

        rule_id = raw_recorder_status['name']
        return rule_id, raw_recorder_status


class Rules(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(Rules, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_rules = await self.facade.config.get_rules(self.region)
        for raw_rule in raw_rules:
            name, resource = self._parse_rule(raw_rule)
            self[name] = resource

    def _parse_rule(self, raw_rule):
        raw_rule['arn'] = raw_rule.pop('ConfigRuleArn')
        raw_rule['name'] = raw_rule.pop('ConfigRuleName')

        # Drop some data
        for key in ['ConfigRuleState']:
            if key in raw_rule:
                raw_rule.pop(key)

        rule_id = raw_rule['name']
        return rule_id, raw_rule


class Config(Regions):
    _children = [
        (RecorderStatus, 'recorders'),
        (Rules, 'rules')
    ]

    def __init__(self, facade: AWSFacade):
        super(Config, self).__init__('config', facade)
