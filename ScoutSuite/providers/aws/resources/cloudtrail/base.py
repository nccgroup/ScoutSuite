from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions

from .trails import Trails


class CloudTrail(Regions):
    _children = [
        (Trails, 'trails')
    ]

    def __init__(self, facade: AWSFacade):
        super(CloudTrail, self).__init__('cloudtrail', facade)
