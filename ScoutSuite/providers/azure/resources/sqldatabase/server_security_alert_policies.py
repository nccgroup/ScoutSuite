from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class ServerSecurityAlertPolicies(AzureResources):

    def __init__(self, facade: AzureFacade, resource_group_name: str, server_name: str, subscription_id: str):
        super(ServerSecurityAlertPolicies, self).__init__(facade)
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.subscription_id = subscription_id

    async def fetch_all(self):
        policies = await self.facade.sqldatabase.get_server_security_alert_policies(
            self.resource_group_name, self.server_name, self.subscription_id)
        self._parse_policies(policies)

    def _parse_policies(self, policies):
        self.update({
            'threat_detection_enabled': policies.state == "Enabled",
            'alerts_enabled': policies.disabled_alerts == [""],
            'send_alerts_enabled': policies.email_addresses != [""] and policies.email_account_admins,
            'retention_days': policies.retention_days
        })
