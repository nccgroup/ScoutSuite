from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.utils import get_name


class FlowLogs(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        self.region = region

        super(FlowLogs, self).__init__(facade)

    async def fetch_all(self):
        raw_logs = await self.facade.ec2.get_flow_logs(self.region)
        for raw_log in raw_logs:
            id, log = self._parse_log(raw_log)
            self[id] = log

    def _parse_log(self, raw_log):
        get_name(raw_log, raw_log, 'FlowLogId')
        log_id = raw_log.pop('FlowLogId')
        return log_id, raw_log
