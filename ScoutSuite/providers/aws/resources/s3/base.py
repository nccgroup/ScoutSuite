from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from .buckets import Buckets


class S3(AWSCompositeResources):
    _children = [
        (Buckets, 'buckets')
    ]

    def __init__(self, facade: AWSFacade):
        super(S3, self).__init__(facade)
        self.service = 's3'

    async def fetch_all(self, partition_name='aws', **kwargs):
        # Keep track of regions as S3 is both a global and regional service
        self.facade.s3.regions = kwargs.get('regions')

        await self._fetch_children(self)
