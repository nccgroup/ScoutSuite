from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions

from .vpcs import ELBVpcs
from .policies import Policies


class ELB(Regions):
    _children = [
        (ELBVpcs, 'vpcs'),
        (Policies, 'elb_policies')
    ]

    def __init__(self, facade: AWSFacade):
        super().__init__('elb', facade)
