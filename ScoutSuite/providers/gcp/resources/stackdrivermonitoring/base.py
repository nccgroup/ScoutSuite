from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.stackdrivermonitoring.monitored_resources import MonitoredResources


class StackdriverMonitoring(Projects):
    _children = [ 
        (MonitoredResources, 'monitored_resources'),
    ]
