from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources

class KMS(AWSCompositeResources):
    _children = [
        (Aliases, 'aliases')
    ]

    def __init__(self, facade: AWSFacade):
        super(KMS, self).__init__(facade)
        self.service = 'kms'

    async def fetch_all(self, partition_name='aws', **kwargs):
        await self._fetch_children(self)
