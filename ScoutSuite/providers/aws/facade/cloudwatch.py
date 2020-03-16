from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class CloudWatch(AWSBaseFacade):
    async def get_alarms(self, region):
        try:
            return await AWSFacadeUtils.get_all_pages('cloudwatch', region, self.session, 'describe_alarms',
                                                      'MetricAlarms')
        except Exception as e:
            print_exception('Failed to get CloudWatch alarms: {}'.format(e))
            return []
