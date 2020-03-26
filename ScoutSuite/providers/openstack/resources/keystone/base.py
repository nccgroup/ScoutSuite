from ScoutSuite.providers.openstack.facade.base import OpenstackFacade
from ScoutSuite.providers.openstack.resources.base import OpenstackCompositeResources
from ScoutSuite.providers.openstack.resources.keystone.policies import Policies


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
