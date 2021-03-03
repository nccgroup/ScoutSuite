from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class ActivityLogAlerts(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        log_alerts = await self.facade.loggingmonitoring.get_activity_log_alerts(self.subscription_id)
        self[self.subscription_id] = self._parse_log_alerts(log_alerts)

    def _parse_log_alerts(self, log_alerts):
        log_alerts_dict = {}
        log_alerts_dict['create_policy_assignment_exist'] = self.ensure_alert_exist(log_alerts,
                                                                                    'microsoft.authorization'
                                                                                    '/policyassignments/write')
        log_alerts_dict['create_update_NSG_exist'] = self.ensure_alert_exist(log_alerts,
                                                                             'microsoft.network/networksecuritygroups'
                                                                             '/write')
        log_alerts_dict['delete_NSG_exist'] = self.ensure_alert_exist(log_alerts,
                                                                      'microsoft.network/networksecuritygroups/delete')
        log_alerts_dict['create_update_NSG_rule_exist'] = self.ensure_alert_exist(log_alerts,
                                                                                   'microsoft.network'
                                                                                   '/networksecuritygroups '
                                                                                   '/securityrules/write')
        log_alerts_dict['delete_NSG_rule_exist'] = self.ensure_alert_exist(log_alerts,
                                                                           'microsoft.network/networksecuritygroups'
                                                                           '/securityrules/delete')
        log_alerts_dict['create_update_security_solution_exist'] = self.ensure_alert_exist(log_alerts,
                                                                                           'microsoft.security'
                                                                                           '/securitysolutions/write')
        log_alerts_dict['delete_security_solution_exist'] = self.ensure_alert_exist(log_alerts,
                                                                           'microsoft.security/securitysolutions/delete')
        log_alerts_dict['create_delete_firewall_rule_exist'] = self.ensure_alert_exist(log_alerts,
                                                                                       'microsoft.sql/servers'
                                                                                       '/firewallrules/write')

        return log_alerts_dict

    def ensure_alert_exist(self, log_alerts, equals_value: str):
        for log_alert in log_alerts:
            if log_alert.location == 'Global' and log_alert.enabled:
                if '/subscriptions/' + self.subscription_id in log_alert.scopes:
                    for condition in log_alert.condition.all_of:
                        if condition.field == 'operationName' and condition.equals == equals_value:
                            return True
        return False
