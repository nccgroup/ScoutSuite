from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions

from .domains import Domains


class Route53(Regions):
    _children = [
        (Domains, 'domains')
    ]

    def __init__(self, facade: AWSFacade):
        super(Route53, self).__init__('route53domains', facade)
