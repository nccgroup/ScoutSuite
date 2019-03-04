from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class CloudWatch:
    def get_alarms(self, region):
        return AWSFacadeUtils.get_all_pages('cloudwatch', region, 'describe_alarms', 'MetricAlarms')
