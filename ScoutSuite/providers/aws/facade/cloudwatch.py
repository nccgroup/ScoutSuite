from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade


class CloudWatch(AWSBaseFacade):
    async def get_alarms(self, region):
        return await AWSFacadeUtils.get_all_pages('cloudwatch', region, self.session, 'describe_alarms', 'MetricAlarms')
