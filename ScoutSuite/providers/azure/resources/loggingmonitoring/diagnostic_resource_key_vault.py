from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class DiagnosticResourceKeyVault(AzureResources):

    def __init__(self, facade: AzureFacade, resource_id: str, subscription_id: str):
        super().__init__(facade)
        self.resource_id = resource_id
        self.subscription_id = subscription_id

    async def fetch_all(self):
        diagnostic_settings = await self.facade.loggingmonitoring.get_diagnostic_settings(self.subscription_id,
                                                                                          self.resource_id)
        self._parse_diagnostic_settings(diagnostic_settings)

    def _parse_diagnostic_settings(self, diagnostic_settings):
        self.update({
            'audit_event_enabled': self.ensure_audit_event_enabled(diagnostic_settings)
        })

    def ensure_audit_event_enabled(self, diagnostic_settings):
        for diagnostic_setting in diagnostic_settings:
            for log in diagnostic_setting.logs:
                if log.category == 'AuditEvent' and log.enabled and log.retention_policy.days > 0:
                    return True
        return False
