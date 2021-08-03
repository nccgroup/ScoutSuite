from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions
from .stacks import Stacks
from .stacksets import StackSets


class CloudFormation(Regions):
    _children = [
        (Stacks, 'stacks'),
        (StackSets, 'stacksets')
    ]

    def __init__(self, facade: AWSFacade):
        super().__init__('cloudformation', facade)
