from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions

from .aliases import Aliases
from .keys import Keys


class KMS(Regions):
    _children = [
        (Aliases, 'aliases'),
        (Keys, 'keys'),
    ]

    def __init__(self, facade: AWSFacade):
        super(KMS, self).__init__('kms', facade)
