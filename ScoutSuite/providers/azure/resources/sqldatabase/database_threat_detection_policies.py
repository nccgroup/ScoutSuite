from ScoutSuite.providers.azure.resources.base import AzureResources


class DatabaseThreatDetectionPolicies(AzureResources):
    async def fetch_all(self):
        policies = await self.facade.sqldatabase.get_database_threat_detection_policies(
            self.scope['resource_group_name'], self.scope['server_name'], self.scope['database_name'])
        self._parse_policies(policies)

    def _parse_policies(self, policies):
        self.update({
            'threat_detection_enabled': policies.state == "Enabled",
            'alerts_enabled': policies.disabled_alerts == "",
            'send_alerts_enabled': policies.email_addresses != "" and policies.email_account_admins == "Enabled",
            'retention_days': policies.retention_days
        })
