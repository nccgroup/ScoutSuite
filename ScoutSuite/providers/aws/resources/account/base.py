from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from .contacts import Contacts

class Account(AWSCompositeResources):
    _children = [
        (Contacts, 'contacts')
    ]

    def __init__(self, facade: AWSFacade):
        super().__init__(facade)
        self.service = 'account'

    async def fetch_all(self, partition_name='aws', **kwargs):
        await self._fetch_children(self)
