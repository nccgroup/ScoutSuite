from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.iam.service_accounts import ServiceAccounts


class IAM(Projects):
    _children = [ 
        (ServiceAccounts, 'service_accounts') 
    ]
