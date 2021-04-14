from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.cloudfront.distributions import Distributions

from .distributions import Distributions


class CloudFront(AWSCompositeResources):
    _children = [
        (Distributions, 'distributions')
    ]

    def __init__(self, facade: AWSFacade):
        super(CloudFront, self).__init__(facade)
        self.service = 'cloudfront'

    async def fetch_all(self, partition_name='aws', **kwargs):
        await self._fetch_children(self)
