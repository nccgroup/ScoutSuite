from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources

from .domains import Route53Domains
from .hosted_zones import Route53HostedZones


class Route53(AWSCompositeResources):
    _children = [
        (Route53Domains, 'domains'),
        (Route53HostedZones, 'hosted_zones')
    ]

    def __init__(self, facade: AWSFacade):
        super(Route53, self).__init__(facade)
        self.service = 'route53'

    async def fetch_all(self, regions=None, partition_name='aws'):
        await self._fetch_children(self)
