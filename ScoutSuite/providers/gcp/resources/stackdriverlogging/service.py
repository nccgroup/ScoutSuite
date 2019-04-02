from ScoutSuite.providers.gcp.facade.gcp import GCPFacade
from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.stackdriverlogging.sinks import Sinks

class StackdriverLogging(Projects):
    _children = [ 
        (Sinks, 'sinks') 
    ]

    def __init__(self, gcp_facade: GCPFacade):
        super(StackdriverLogging, self).__init__(gcp_facade)
