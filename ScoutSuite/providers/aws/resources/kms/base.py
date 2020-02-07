from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions
from ScoutSuite.providers.aws.resources.kms.aliases import Aliases

from .aliases import Aliases

class KMS(Regions):
    _children = [
        (Aliases, 'aliases')
    ]

    def __init__(self, facade: AWSFacade):
        super(KMS, self).__init__('kms', facade)

