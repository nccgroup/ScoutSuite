# -*- coding: utf-8 -*-

from ..resources import AzureSimpleResources


class ServerBlobAuditingPolicies(AzureSimpleResources):

    def __init__(self, resource_group_name, server_name, facade):
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.facade = facade

    # TODO: make it really async.
    async def get_resources_from_api(self):
        return self.facade.server_blob_auditing_policies.get(
            self.resource_group_name, self.server_name)

    def parse_resource(self, policies):
        return 'auditing_enabled', policies.state == "Enabled"
