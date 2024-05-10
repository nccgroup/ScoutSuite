from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.do.authentication_strategy import DoCredentials
from ScoutSuite.providers.do.facade.utils import DOFacadeUtils
from ScoutSuite.providers.utils import run_concurrently


class Networkingfacade:
    def __init__(self, credentials: DoCredentials):
        self._credentials = credentials
        self._client = credentials.client
        self.current_page = 1
        self.per_page = 50

    async def get_firewalls(self):
        try:
            firewalls = await DOFacadeUtils.get_all_from_pagination(
                self._client.firewalls.list,
                self.current_page,
                self.per_page,
                "firewalls",
            )
            return firewalls["firewalls"]
        except Exception as e:
            print_exception(f"Failed to get firewalls: {e}")
            return []

    async def get_domains(self):
        try:
            domains = await DOFacadeUtils.get_all_from_pagination(
                self._client.domains.list, self.current_page, self.per_page, "domains"
            )
            return domains["domains"]
        except Exception as e:
            print_exception(f"Failed to get domains: {e}")
            return []

    async def get_load_balancers(self):
        try:
            load_balancers = await DOFacadeUtils.get_all_from_pagination(
                self._client.load_balancers.list,
                self.current_page,
                self.per_page,
                "load_balancers",
            )
            return load_balancers["load_balancers"]
        except Exception as e:
            print_exception(f"Failed to get load balancers: {e}")
            return []
