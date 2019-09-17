from ScoutSuite.providers.os.facade.base import OpenstackFacade
from ScoutSuite.providers.os.resources.base import OpenstackResources


class Policies(OpenstackResources):
    def __init__(self, facade: OpenstackFacade):
        super(Policies, self).__init__(facade)

    async def fetch_all(self):
        self['isFernet'] = self.facade.keystone.is_fernet()
