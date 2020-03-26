from ScoutSuite.providers.openstack.facade.keystone import KeystoneFacade
from ScoutSuite.providers.openstack.authentication_strategy import OpenstackCredentials


class OpenstackFacade:
    def __init__(self, credentials: OpenstackCredentials):
        self._credentials = credentials
        self._instantiate_facades()

    def _instantiate_facades(self):
        self.keystone = KeystoneFacade(self._credentials)