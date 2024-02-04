from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.do.authentication_strategy import DoCredentials
from ScoutSuite.providers.utils import run_concurrently


class Networkingfacade:
    def __init__(self, credentials: DoCredentials):
        self._credentials = credentials
        self._client = credentials.client

    async def get_firewalls(self):
        try:
            firewalls = await run_concurrently(
                lambda: self._client.firewalls.list()["firewalls"]
            )
            return firewalls
        except Exception as e:
            print_exception(f"Failed to get firewalls: {e}")
            return []

    async def get_domains(self):
        try:
            domains = await run_concurrently(
                lambda: self._client.domains.list()["domains"]
            )
            return domains
        except Exception as e:
            print_exception(f"Failed to get domains: {e}")
            return []

    async def get_load_balancers(self):
        try:
            load_balancers = await run_concurrently(
                lambda: self._client.load_balancers.list()["load_balancers"]
            )
            return load_balancers
        except Exception as e:
            print_exception(f"Failed to get load balancers: {e}")
            return []
