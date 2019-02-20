# -*- coding: utf-8 -*-

from azure.mgmt.sql import SqlManagementClient

from ScoutSuite.providers.base.configs.resource_config import ResourceConfig

from .database_blob_auditing_policies import DatabaseBlobAuditingPoliciesConfig
from .database_threat_detection_policies import DatabaseThreatDetectionPoliciesConfig
from .replication_links import ReplicationLinksConfig
from .transparent_data_encryptions import TransparentDataEncryptionsConfig


class DatabasesConfig(ResourceConfig):
    # the following static methods will be used to parse the config of each resource nested in a database config
    # (defined in 'children' attribute below):
    @staticmethod
    def _parse_auditing_config(config):
        return {
            'auditing_enabled': config.value.state == "Enabled"
        }

    @staticmethod
    def _parse_threat_detection_config(config):
        return {
            'threat_detection_enabled': config.value.state == "Enabled"
        }

    @staticmethod
    def _parse_replication_links_config(config):
        return {
            'replication_configured': len(config.value) > 0
        }

    @staticmethod
    def _parse_transparent_data_encryption_config(config):
        return {
            'transparent_data_encryption_enabled': config.value.status == "Enabled"
        }

    # register children resources:
    children = [
        (DatabaseBlobAuditingPoliciesConfig, _parse_auditing_config),
        (DatabaseThreatDetectionPoliciesConfig, _parse_threat_detection_config),
        (ReplicationLinksConfig, _parse_replication_links_config),
        (TransparentDataEncryptionsConfig, _parse_transparent_data_encryption_config)
    ]

    def __init__(self, resource_group_name, server_name):
        self.resource_group_name = resource_group_name
        self.server_name = server_name

        self.databases = {}

    async def fetch_all(self, credentials, regions=None, partition_name='aws', targets=None):
        # sdk container:
        api = SqlManagementClient(credentials.credentials, credentials.subscription_id)

        # TODO: for db in await api.databases.list_by_server(self.resource_group_name, self.server_name):
        for db in api.databases.list_by_server(self.resource_group_name, self.server_name):
            self.databases[db.name] = {
                'id': db.name,
            }

            # put the following code in a fetch_children() parent method (typical method for a composite node)?
            for (resource_config, resource_parser) in self.children:
                resource = resource_config(self.resource_group_name, self.server_name, db.name)
                await resource.fetch_all(credentials)
                for k, v in resource_parser.__func__(resource).items():
                    self.databases[db.name][k] = v
