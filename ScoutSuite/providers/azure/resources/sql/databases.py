# -*- coding: utf-8 -*-

from azure.mgmt.sql import SqlManagementClient

from ScoutSuite.providers.base.configs.resources import Resources

from .database_blob_auditing_policies import DatabaseBlobAuditingPolicies
from .database_threat_detection_policies import DatabaseThreatDetectionPolicies
from .replication_links import ReplicationLinks
from .transparent_data_encryptions import TransparentDataEncryptions


class Databases(Resources):
    children = [
        DatabaseBlobAuditingPolicies,
        DatabaseThreatDetectionPolicies,
        ReplicationLinks,
        TransparentDataEncryptions,
    ]

    def __init__(self, resource_group_name, server_name):
        self.resource_group_name = resource_group_name
        self.server_name = server_name

    async def fetch_all(self, credentials):
        # sdk container:
        api = SqlManagementClient(credentials.credentials, credentials.subscription_id)

        self['databases'] = {}
        # TODO: for db in await api.databases.list_by_server(self.resource_group_name, self.server_name):
        for db in api.databases.list_by_server(self.resource_group_name, self.server_name):
            self['databases'][db.name] = {
                'id': db.name,
            }

            # put the following code in a fetch_children() parent method (typical method for a composite node)?
            for resources_class in self.simple_children:
                resources = resources_class(self.resource_group_name, self.server_name, db.name)
                await resources.fetch_all(credentials)
                self['databases'][db.name].update(resources)
