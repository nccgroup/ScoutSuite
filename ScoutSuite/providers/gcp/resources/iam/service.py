# -*- coding: utf-8 -*-

from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.iam.service_accounts import ServiceAccounts

class IAM(Projects):
    _children = [ 
        (ServiceAccounts, 'service_accounts') 
    ]

    def __init__(self, gcp_facade):
        super(IAM, self).__init__(gcp_facade)
