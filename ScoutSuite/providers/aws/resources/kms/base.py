from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions

from .aliases import Aliases
from .grants import Grants
from .keys import Keys
from .key_policies import KeyPolicies


class KMS(Regions):
    _children = [
        (Aliases, 'aliases'),
        (Keys, 'keys'),
        (Grants, 'grants'),
        (KeyPolicies, 'key_policies')
    ]

    def __init__(self, facade: AWSFacade):
        super(KMS, self).__init__('kms', facade)
