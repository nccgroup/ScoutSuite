from ScoutSuite.providers.salesforce.facade.base import SalesforceFacade
from ScoutSuite.providers.salesforce.resources.base import SalesforceCompositeResources
from ScoutSuite.providers.salesforce.resources.profiles.profiles import Profiles


class Profiles(SalesforceCompositeResources):
    _children = [
        (Profiles, 'profiles')
    ]

    def __init__(self, facade: SalesforceFacade):
        super(Profiles, self).__init__(facade)
        self.service = 'profiles'

    async def fetch_all(self, **kwargs):
        await self._fetch_children(resource_parent=self)
