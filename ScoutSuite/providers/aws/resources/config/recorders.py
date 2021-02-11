from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class Recorders(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_recorders = await self.facade.config.get_recorders(self.region)
        parsing_error_counter = 0
        for raw_recorder in raw_recorders:
            try:
                name, resource = self._parse_recorder(raw_recorder)
                self[name] = resource
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_recorder(self, raw_recorder):
        recorder = {}
        recorder['name'] = raw_recorder['name']
        recorder['region'] = self.region
        recorder['role_ARN'] = raw_recorder['roleARN']
        recorder['recording_group'] = raw_recorder['recordingGroup']
        recorder['enabled'] = raw_recorder['ConfigurationRecordersStatus']['recording']
        recorder['last_status'] = raw_recorder['ConfigurationRecordersStatus'].get('lastStatus')
        recorder['last_start_time'] = raw_recorder['ConfigurationRecordersStatus'].get('lastStartTime')
        recorder['last_status_change_time'] = raw_recorder['ConfigurationRecordersStatus'].get('lastStatusChangeTime')
        return recorder['name'], recorder
