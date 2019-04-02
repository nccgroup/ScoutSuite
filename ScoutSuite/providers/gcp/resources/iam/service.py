from ScoutSuite.providers.gcp.facade.gcp import GCPFacade
from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.iam.service_accounts import ServiceAccounts

class IAM(Projects):
    _children = [ 
        (ServiceAccounts, 'service_accounts') 
    ]

    def __init__(self, gcp_facade: GCPFacade):
        super(IAM, self).__init__(gcp_facade)
