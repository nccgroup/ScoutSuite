from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.stackdrivermonitoring.monitoring_alert_policies import MonitoringAlertPolicies
from ScoutSuite.providers.gcp.resources.stackdrivermonitoring.uptime_checks import UptimeChecks
from ScoutSuite.providers.gcp.resources.stackdrivermonitoring.alert_policies import AlertPolicies


class StackdriverMonitoring(Projects):
    _children = [ 
        (UptimeChecks, 'uptime_checks'),
        (AlertPolicies, 'alert_policies'),
        (MonitoringAlertPolicies, 'monitoring_alert_policies')
    ]
