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
        super(CloudWatch, self).__init__('cloudwatch', facade)
