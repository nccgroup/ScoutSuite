from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class CloudWatch(AWSBaseFacade):

    async def get_alarms(self, region):
        try:
            return await AWSFacadeUtils.get_all_pages('cloudwatch', region, self.session, 'describe_alarms',
                                                      'MetricAlarms')
        except Exception as e:
            print_exception(f'Failed to get CloudWatch alarms: {e}')
            return []

    async def get_metric_filters(self, region):
        try:
            return await AWSFacadeUtils.get_all_pages('logs', region, self.session, 'describe_metric_filters',
                                                      'metricFilters')
        except Exception as e:
            print_exception('Failed to get CloudWatch metric filters: {}'.format(e))
            return []

