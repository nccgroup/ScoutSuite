from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .log_profiles import LogProfiles
from .diagnostic_settings import DiagnosticSettings
from .activity_log_alerts import ActivityLogAlerts
from.resources import Resources


class LoggingMonitoring(Subscriptions):
    _children = [
        (LogProfiles, 'log_profiles'),
        (DiagnosticSettings, 'diagnostic_settings'),
        (ActivityLogAlerts, 'log_alerts'),
        (Resources, 'resources_logging')
    ]

