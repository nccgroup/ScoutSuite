from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions

from .alarms import Alarms
from .metric_filters import MetricFilters


class CloudWatch(Regions):
    _children = [
        (Alarms, 'alarms'),
        (MetricFilters, 'metric_filters')
    ]

    def __init__(self, facade: AWSFacade):
        super().__init__('cloudwatch', facade)

    async def finalize(self):

        # For each region, check if at least one metric filter covers the desired events
        for region in self['regions']:
            self['regions'][region]['metric_filters_pattern_checks'] = {}
            # Initialize results at "False"
            self['regions'][region]['metric_filters_pattern_checks']['console_login_mfa'] = False
            for metric_filter_id, metric_filter in self['regions'][region]['metric_filters'].items():
                # Check events
                if metric_filter['pattern'] == 'filterPattern": "{ ($.eventName = "ConsoleLogin") && ($.additionalEventData.MFAUsed != "Yes") }':
                    self['regions'][region]['metric_filters_pattern_checks']['console_login_mfa'] = True
