from ScoutSuite.providers.azure.resources.base import AzureResources


class ServerSecurityAlertPolicies(AzureResources):
    async def fetch_all(self):
        policies = await self.facade.sqldatabase.get_server_security_alert_policies(
            self.scope['resource_group_name'], self.scope['server_name'])
        self._parse_policies(policies)

    def _parse_policies(self, policies):
        self.update({
            'threat_detection_enabled': policies.state == "Enabled",
            'alerts_enabled': policies.disabled_alerts == [""],
            'send_alerts_enabled': policies.email_addresses != [""] and policies.email_account_admins,
            'retention_days': policies.retention_days
        })
