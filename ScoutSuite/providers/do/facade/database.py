from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.do.authentication_strategy import DoCredentials
from ScoutSuite.providers.utils import run_concurrently


class DatabasesFacade:
    def __init__(self, credentials: DoCredentials):
        self._credentials = credentials
        self._client = credentials.client

    async def get_databases(self):
        try:
            databases = await run_concurrently(
                lambda: self._client.databases.list_clusters()["databases"]
            )
            return databases
        except Exception as e:
            print_exception(f"Failed to get databases: {e}")
            return []

    async def get_databaseusers(self, db_uuid):
        try:
            db_users = await run_concurrently(
                lambda: self._client.databases.list_users(db_uuid)["users"]
            )
            return db_users
        except Exception as e:
            print_exception(f"Failed to get db users: {e}")
            return []

    async def get_eviction_policy(self, db_uuid):
        try:
            eviction_policy = await run_concurrently(
                lambda: self._client.databases.get_eviction_policy(db_uuid)[
                    "eviction_policy"
                ]
            )
            return eviction_policy
        except Exception as e:
            print_exception(f"Failed to get Redis eviction policy: {e}")
            return []

    async def get_connection_pools(self, db_uuid):
        try:
            connection_pools = await run_concurrently(
                lambda: self._client.databases.list_connection_pools(db_uuid)["pools"]
            )
            return connection_pools
        except Exception as e:
            print_exception(f"Failed to get Postgres connection pools: {e}")
            return []

    async def get_firewalls(self, db_uuid):
        try:
            firewall_rules = await run_concurrently(
                lambda: self._client.databases.list_firewall_rules(db_uuid)
            )
            return firewall_rules
        except Exception as e:
            print_exception(f"Failed to get db firewalls: {e}")
            return []

    async def get_resources(self, tag):
        try:
            resources = await run_concurrently(
                lambda: self._client.tags.get(tag)["tag"]["resources"]
            )
            return resources
        except Exception as e:
            print_exception(f"Failed to get tag resources: {e}")
            return []
