from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.iam.member_bindings import Bindings
from ScoutSuite.providers.gcp.resources.iam.users import Users
from ScoutSuite.providers.gcp.resources.iam.groups import Groups
from ScoutSuite.providers.gcp.resources.iam.service_accounts import ServiceAccounts


class IAM(Projects):
    _children = [
        (Bindings, 'bindings'),
        (Users, 'users'),
        (Groups, 'groups'),
        (ServiceAccounts, 'service_accounts')
    ]
