from ScoutSuite.providers.do.facade.droplet import DropletFacade
from ScoutSuite.providers.do.facade.networking import Networkingfacade
from ScoutSuite.providers.do.facade.database import DatabasesFacade
from ScoutSuite.providers.do.facade.spaces import SpacesFacade
from ScoutSuite.providers.do.facade.kubernetes import KubernetesDoFacade
from ScoutSuite.providers.do.authentication_strategy import DoCredentials


class DoFacade:
    def __init__(self, credentials: DoCredentials):
        self._credentials = credentials
        self._instantiate_facades()

    def _instantiate_facades(self):
        self.droplet = DropletFacade(self._credentials)
        self.networking = Networkingfacade(self._credentials)
        self.database = DatabasesFacade(self._credentials)
        self.spaces = SpacesFacade(self._credentials)
        self.kubernetes = KubernetesDoFacade(self._credentials)
