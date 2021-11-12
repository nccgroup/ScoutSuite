from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.utils import get_name, format_arn


class FlowLogs(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.facade = facade
        self.region = region
        self.partition = facade.partition
        self.service = 'vpc'
        self.resource_type = 'flow-log'

    async def fetch_all(self):
        raw_logs = await self.facade.ec2.get_flow_logs(self.region)

        for raw_log in raw_logs:
            id, log = self._parse_log(raw_log)
            self[id] = log

    def _parse_log(self, raw_flow_log):
        flow_log_dict = {}
        flow_log_dict['name'] = flow_log_dict['id'] = raw_flow_log.get('FlowLogId')
        flow_log_dict['creation_time'] = raw_flow_log.get('CreationTime')
        flow_log_dict['deliver_logs_error_message'] = raw_flow_log.get('DeliverLogsErrorMessage')
        flow_log_dict['deliver_logs_status'] = raw_flow_log.get('DeliverLogsStatus')
        flow_log_dict['flow_log_status'] = raw_flow_log.get('FlowLogStatus')
        flow_log_dict['resource_id'] = raw_flow_log.get('ResourceId')
        flow_log_dict['traffic_type'] = raw_flow_log.get('TrafficType')
        flow_log_dict['log_destination_type'] = raw_flow_log.get('LogDestinationType')
        flow_log_dict['log_destination'] = raw_flow_log.get('LogDestination')
        flow_log_dict['log_format'] = raw_flow_log.get('LogFormat')
        flow_log_dict['tags'] = raw_flow_log.get('Tags')
        flow_log_dict['max_aggregation_interval'] = raw_flow_log.get('MaxAggregationInterval')
        flow_log_dict['arn'] = format_arn(self.partition, self.service, self.region, '', raw_flow_log.get('FlowLogId'), self.resource_type)
        return flow_log_dict['id'], flow_log_dict

