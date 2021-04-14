from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.stackdriverlogging.logging_metrics import LoggingMetrics
from ScoutSuite.providers.gcp.resources.stackdriverlogging.sinks import Sinks
from ScoutSuite.providers.gcp.resources.stackdriverlogging.metrics import Metrics


class StackdriverLogging(Projects):
    _children = [ 
        (Sinks, 'sinks'),
        (Metrics, 'metrics'),
        (LoggingMetrics, 'logging_metrics')
    ]
