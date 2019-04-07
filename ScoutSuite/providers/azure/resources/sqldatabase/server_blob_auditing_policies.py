from ScoutSuite.providers.azure.resources.base import AzureResources


class ServerBlobAuditingPolicies(AzureResources):
    async def fetch_all(self):
        policies = await self.facade.sqldatabase.get_server_blob_auditing_policies(
            self.scope['resource_group_name'], self.scope['server_name'])
        self._parse_policies(policies)

    def _parse_policies(self, policies):
        self.update({
            'auditing_enabled': policies.state == "Enabled",
            'retention_days': policies.retention_days
        })
