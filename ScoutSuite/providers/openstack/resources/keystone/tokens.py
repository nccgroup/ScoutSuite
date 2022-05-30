from ScoutSuite.providers.openstack.facade.base import OpenstackFacade
from ScoutSuite.providers.openstack.resources.base import OpenstackResources


class Tokens(OpenstackResources):
    def __init__(self, facade: OpenstackFacade):
        super(Tokens, self).__init__(facade)

    async def fetch_all(self):
        self['isFernet'] = await self.facade.keystone.is_fernet()
