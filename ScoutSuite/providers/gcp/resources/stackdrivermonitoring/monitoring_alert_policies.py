from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade


class MonitoringAlertPolicies(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_alert_policies = await self.facade.stackdrivermonitoring.get_alert_policies(self.project_id)
        alert_policy = self._parse_alert_policy(raw_alert_policies)
        self[self.project_id] = alert_policy

    def _parse_alert_policy(self, raw_alert_policies):
        alert_policy_dict = {}
        alert_policy_dict['project_ownership_assignments'] = \
            self._specific_alert_policy_present(raw_alert_policies, 'project_ownership_changes-counter')
        alert_policy_dict['audit_config_change'] = \
            self._specific_alert_policy_present(raw_alert_policies, 'audit_config_change-counter')
        alert_policy_dict['custom_role_change'] = \
            self._specific_alert_policy_present(raw_alert_policies, 'custom_role_changes-counter')
        alert_policy_dict['vpc_network_firewall_rule_change'] = \
            self._specific_alert_policy_present(raw_alert_policies, 'vpc_firewall_network_changes-counter')
        alert_policy_dict['vpc_network_route_change'] = \
            self._specific_alert_policy_present(raw_alert_policies, 'vpc_network_route_changes-counter')
        alert_policy_dict['vpc_network_change'] = \
            self._specific_alert_policy_present(raw_alert_policies, 'vpc_network_configuration_changes-counter')
        alert_policy_dict['cloud_storage_iam_permission_change'] = \
            self._specific_alert_policy_present(raw_alert_policies, 'cloud_storage_iam_changes-counter')
        alert_policy_dict['sql_instance_conf_change'] = \
            self._specific_alert_policy_present(raw_alert_policies, 'sql_instance_configuration_changes-counter')
        return alert_policy_dict

    def _specific_alert_policy_present(self, alert_policies, metric_name):
        expected_fragment = 'logging.googleapis.com/user/{}'.format(metric_name)
        for alert_policy in alert_policies:
            if not alert_policy.enabled.value:
                continue
            for condition in alert_policy.conditions:
                if expected_fragment in condition.condition_threshold.filter:
                    return True
        return False
