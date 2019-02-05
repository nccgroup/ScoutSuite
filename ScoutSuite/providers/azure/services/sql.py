# -*- coding: utf-8 -*-

from ScoutSuite.providers.azure.configs.base import AzureBaseConfig
from ScoutSuite.providers.azure.utils import get_resource_group_name

class SQLConfig(AzureBaseConfig):
    targets = (
        ('servers', 'Servers', 'list', {}, False),
    )

    def __init__(self, thread_config):

        self.servers = {}
        self.servers_count = 0

        super(SQLConfig, self).__init__(thread_config)

    def parse_servers(self, server, params):
        server_dict = {}
        server_dict['id'] = self.get_non_provider_id(server.id)
        server_dict['name'] = server.name
        server_dict['databases'] = self._parse_databases(server)

        self.servers[server_dict['id']] = server_dict

    def _parse_databases(self, server):
        databases = {}
        for db in server.databases:
            # Azure automatically creates a reserved read-only 'master' database to manage an SQL server, ignore it:
            if db.name == "master":
                continue

            db_dict = {}
            db_dict['id'] = db.name
            db_dict['auditing_enabled'] = self._is_auditing_enabled(db)
            db_dict['threat_detection_enabled'] = self._is_threat_detection_enabled(db)
            databases[db.name] = db_dict

        return databases

    def _is_auditing_enabled(self, db):
        return db.auditing_settings.state == "Enabled"

    def _is_threat_detection_enabled(self, db):
        return db.threat_detection_settings.state == "Enabled"

    def _get_targets(self, response_attribute, api_client, method, list_params, ignore_list_error):
        if response_attribute == "Servers":
            return self._get_servers(api_client, method, list_params)
        else:
            return super(SQLConfig, self)._get_targets(response_attribute, api_client, method,
                                                                   list_params, ignore_list_error)

    def _get_servers(self, api_client, method, list_params):
        servers = []
        servers_raw = method(**list_params)
        for server in servers_raw:
            resource_group_name = get_resource_group_name(server.id)
            setattr(server, "databases",
                    self._get_databases(api_client, resource_group_name, server.name))
            servers.append(server)

        return servers

    def _get_databases(self, api_client, resource_group_name, server_name):
        databases = []
        databases_raw = api_client.databases.list_by_server(resource_group_name, server_name)
        for db in databases_raw:
            setattr(db, "auditing_settings",
                    self._get_auditing_settings(api_client, resource_group_name, server_name, db.name))
            setattr(db, "threat_detection_settings",
                    self._get_threat_detection_settings(api_client, resource_group_name, server_name, db.name))
            databases.append(db)

        return databases

    def _get_auditing_settings(self, api_client, resource_group_name, server_name, database_name):
        return api_client.database_blob_auditing_policies.get(resource_group_name, server_name, database_name)

    def _get_threat_detection_settings(self, api_client, resource_group_name, server_name, database_name):
        return api_client.database_threat_detection_policies.get(resource_group_name, server_name, database_name)
