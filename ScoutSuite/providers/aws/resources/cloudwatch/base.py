from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions

from .alarms import Alarms


class CloudWatch(Regions):
    _children = [
        (Alarms, 'alarms')
    ]

    def __init__(self, facade: AWSFacade):
        super(CloudWatch, self).__init__('cloudwatch', facade)
