from ScoutSuite.providers.do.authentication_strategy import DoCredentials
from ScoutSuite.providers.do.resources.droplet.base import Droplets
from ScoutSuite.providers.do.resources.spaces.base import Spaces
from ScoutSuite.providers.do.resources.networking.base import Networking
from ScoutSuite.providers.do.resources.database.base import Databases
from ScoutSuite.providers.do.resources.kubernetes.base import Kubernetes
from ScoutSuite.providers.do.facade.base import DoFacade
from ScoutSuite.providers.base.services import BaseServicesConfig


class DigitalOceanServicesConfig(BaseServicesConfig):
    def __init__(self, credentials: DoCredentials = None, **kwargs):
        super().__init__(credentials)

        facade = DoFacade(credentials)

        self.droplet = Droplets(facade)
        self.networking = Networking(facade)
        self.database = Databases(facade)
        self.kubernetes = Kubernetes(facade)
        if self.credentials.session:
            self.spaces = Spaces(facade)

    def _is_provider(self, provider_name):
        return provider_name == "do"
