from ScoutSuite.providers.do.resources.base import DoResources
from ScoutSuite.providers.do.facade.base import DoFacade


class Databases(DoResources):
    def __init__(self, facade: DoFacade):
        super().__init__(facade)

    async def fetch_all(self):
        clusters = await self.facade.database.get_databases()
        if clusters:
            for cluster in clusters:
                id, cluster = await self._parse_cluster(cluster)
                self[id] = cluster

    async def _parse_cluster(self, raw_cluster):
        cluster_dict = {}

        cluster_dict["id"] = raw_cluster["id"]
        cluster_dict["name"] = raw_cluster["name"]
        cluster_dict["engine"] = raw_cluster["engine"]
        cluster_dict["version"] = raw_cluster["version"]
        if raw_cluster["engine"] != "mongodb":
            cluster_dict["semantic_version"] = raw_cluster["semantic_version"]
        cluster_dict["tags"] = raw_cluster["tags"]
        cluster_dict["databases"] = str(raw_cluster["db_names"])

        trusted_sources = set()
        cluster_databases = await self.facade.database.get_firewalls(raw_cluster["id"])
        if cluster_databases:
            for cluster_rule in cluster_databases["rules"]:
                trusted_sources.add(f"{cluster_rule['type']}s:{cluster_rule['value']}")

        cluster_dict["trusted_sources"] = (
            trusted_sources if trusted_sources else "False"
        )

        if raw_cluster["engine"] == "mysql":
            legacy_encryption_users = set()
            db_users = await self.facade.database.get_databaseusers(raw_cluster["id"])
            if db_users:
                for db_user in db_users:
                    if (
                        db_user["mysql_settings"]["auth_plugin"]
                        == "mysql_native_password"
                    ):
                        legacy_encryption_users.add(db_user["name"])
            if legacy_encryption_users == "None":
                cluster_dict["legacy_encryption_users"] = "True"
            else:
                cluster_dict["legacy_encryption_users"] = (
                    str(legacy_encryption_users) if legacy_encryption_users else "False"
                )
        elif raw_cluster["engine"] == "redis":
            cluster_dict["eviction_policy"] = (
                await self.facade.database.get_eviction_policy(raw_cluster["id"])
            )

        elif raw_cluster["engine"] == "pg":
            connection_pools = await self.facade.database.get_connection_pools(
                raw_cluster["id"]
            )
            cluster_dict["connection_pools"] = (
                connection_pools if connection_pools else "False"
            )
        return cluster_dict["id"], cluster_dict
