from ScoutSuite.providers.base.configs.resources import Resources


class ServerSecurityAlertPolicies(Resources):

    def __init__(self, resource_group_name, server_name, facade):
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.facade = facade

    async def fetch_all(self):
        policies = await self.facade.get_server_security_alert_policies(
            self.resource_group_name, self.server_name)
        self._parse_policies(policies)

    def _parse_policies(self, policies):
        self.update({
            'threat_detection_enabled': policies.state == "Enabled",
            'alerts_enabled': policies.disabled_alerts == [""],
            'send_alerts_enabled': policies.email_addresses != [""] and policies.email_account_admins,
            'retention_days': policies.retention_days
        })
