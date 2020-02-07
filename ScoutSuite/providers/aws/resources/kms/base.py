from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions

from .aliases import Aliases
from .grants import Grants

class KMS(Regions):
    _children = [
        (Aliases, 'aliases'),
        (Grants, 'grants')
    ]

    def __init__(self, facade: AWSFacade):
        super(KMS, self).__init__('kms', facade)

