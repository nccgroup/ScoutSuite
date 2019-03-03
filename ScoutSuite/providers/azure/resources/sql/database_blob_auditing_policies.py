# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.resources import Resources


class DatabaseBlobAuditingPolicies(Resources):

    def __init__(self, resource_group_name, server_name, database_name, facade):
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name
        self.facade = facade

    # TODO: make it really async.
    async def fetch_all(self):
        policies = self.facade.database_blob_auditing_policies.get(
            self.resource_group_name, self.server_name, self.database_name)
        self._parse_policies(policies)

    def _parse_policies(self, policies):
        self.update({
            'auditing_enabled': policies.state == "Enabled"
        })
