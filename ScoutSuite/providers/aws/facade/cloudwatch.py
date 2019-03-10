from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class CloudWatch:
    async def get_alarms(self, region):
        return await AWSFacadeUtils.get_all_pages('cloudwatch', region, 'describe_alarms', 'MetricAlarms')
