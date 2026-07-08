from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions
from ScoutSuite.providers.azure.resources.loggingmonitoring.log_profiles import LogProfiles
from ScoutSuite.providers.azure.resources.loggingmonitoring.diagnostic_settings import DiagnosticSettings
from ScoutSuite.providers.azure.resources.loggingmonitoring.activity_log_alerts import ActivityLogAlerts
from ScoutSuite.providers.azure.resources.loggingmonitoring.resources import Resources


class AKS(Subscriptions):
    _children = [
        (LogProfiles, 'log_profiles'),
        (DiagnosticSettings, 'diagnostic_settings'),
        (ActivityLogAlerts, 'log_alerts'),
        (Resources, 'resources_logging')
    ]
