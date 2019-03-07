# -*- coding: utf-8 -*-

from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.stackdriverlogging.sinks import Sinks

class StackdriverLogging(Projects):
    _children = [ 
        ('sinks', Sinks) 
    ]

    def __init__(self, gcp_facade, sdl_facade):
        super(StackdriverLogging, self).__init__(gcp_facade, sdl_facade)
