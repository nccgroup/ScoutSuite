from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .log_profiles import LogProfiles
from .diagnostic_settings import DiagnosticSettings


class LoggingMonitoring(Subscriptions):
    _children = [
        # (LogProfiles, 'log_profiles'),
        # (DiagnosticSettings, 'diagnostic_settings')
    ]
