from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions

from .vpcs import ELBVpcs


class ELB(Regions):
    _children = [
        (ELBVpcs, 'vpcs')
    ]

    def __init__(self, facade: AWSFacade):
        super(ELB, self).__init__('elb', facade)
