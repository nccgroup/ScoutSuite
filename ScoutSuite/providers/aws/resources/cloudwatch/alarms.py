from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.core.console import print_exception


class Alarms(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_alarms = await self.facade.cloudwatch.get_alarms(self.region)
        for raw_alarm in raw_alarms:
            try:
                name, resource = self._parse_alarm(raw_alarm)
                self[name] = resource
            except Exception as e:
                print_exception('Failed to parse {} resource: {}'.format(self.__class__.__name__, e))

    def _parse_alarm(self, raw_alarm):
        raw_alarm['arn'] = raw_alarm.pop('AlarmArn')
        raw_alarm['name'] = raw_alarm.pop('AlarmName')

        # Drop some data
        for key in ['AlarmConfigurationUpdatedTimestamp', 'StateReason', 'StateReasonData', 'StateUpdatedTimestamp']:
            if key in raw_alarm:
                raw_alarm.pop(key)

        alarm_id = get_non_provider_id(raw_alarm['arn'])
        return alarm_id, raw_alarm
