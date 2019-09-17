from ScoutSuite.providers.os.facade.base import OpenstackFacade
from ScoutSuite.providers.os.resources.base import OpenstackCompositeResources
from ScoutSuite.providers.os.resources.keystone.policies import Policies


class Keystone(OpenstackCompositeResources):
    _children = [
        (Policies, 'policies'),
    ]

    def __init__(self, facade: OpenstackFacade):
        super(Keystone, self).__init__(facade)
        self.service = 'keystone'

    async def fetch_all(self, **kwargs):
        await self._fetch_children(resource_parent=self)

    async def finalize(self):
        return
