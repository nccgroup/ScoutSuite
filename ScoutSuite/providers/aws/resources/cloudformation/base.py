from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions
from .stacks import Stacks


class CloudFormation(Regions):
    _children = [
        (Stacks, 'stacks')
    ]

    def __init__(self, facade: AWSFacade):
        super(CloudFormation, self).__init__('cloudformation', facade)
