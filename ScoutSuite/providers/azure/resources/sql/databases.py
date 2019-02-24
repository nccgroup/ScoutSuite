# -*- coding: utf-8 -*-

from azure.mgmt.sql import SqlManagementClient

from ..resources import AzureCompositeResources

from .database_blob_auditing_policies import DatabaseBlobAuditingPolicies
from .database_threat_detection_policies import DatabaseThreatDetectionPolicies
from .replication_links import ReplicationLinks
from .transparent_data_encryptions import TransparentDataEncryptions


class Databases(AzureCompositeResources):
    children = [
        DatabaseBlobAuditingPolicies,
        DatabaseThreatDetectionPolicies,
        ReplicationLinks,
        TransparentDataEncryptions,
    ]

    def __init__(self, resource_group_name, server_name):
        self.resource_group_name = resource_group_name
        self.server_name = server_name

    # TODO: make it really async.
    async def fetch_all(self, credentials):
        api = SqlManagementClient(credentials.credentials, credentials.subscription_id)

        self['databases'] = {}
        for db in api.databases.list_by_server(self.resource_group_name, self.server_name):
            self['databases'][db.name] = {
                'id': db.name,
            }
            await self.fetch_children(
                parent=self['databases'][db.name],
                resource_group_name=self.resource_group_name,
                server_name=self.server_name,
                database_name=db.name,
                credentials=credentials
            )
