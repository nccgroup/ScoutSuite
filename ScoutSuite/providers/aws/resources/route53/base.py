from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions

from .domains import Domains
from .hosted_zones import HostedZones


class Route53(Regions):
    _children = [
        (Domains, 'domains'),
        (HostedZones, 'hosted_zones')
    ]

    def __init__(self, facade: AWSFacade):
        super(Route53, self).__init__('route53domains', facade)
