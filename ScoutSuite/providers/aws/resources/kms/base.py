from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions

from .keys import Keys


class KMS(Regions):
    _children = [
        (Keys, 'keys'),
    ]

    def __init__(self, facade: AWSFacade):
        super(KMS, self).__init__('kms', facade)
