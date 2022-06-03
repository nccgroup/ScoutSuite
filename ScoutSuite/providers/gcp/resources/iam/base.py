from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.iam.member_bindings import Bindings
from ScoutSuite.providers.gcp.resources.iam.users import Users
from ScoutSuite.providers.gcp.resources.iam.groups import Groups
from ScoutSuite.providers.gcp.resources.iam.domains import Domains
from ScoutSuite.providers.gcp.resources.iam.service_accounts import ServiceAccounts
from ScoutSuite.providers.gcp.resources.iam.bindings_separation_duties import BindingsSeparationDuties


class IAM(Projects):
    _children = [
        (Bindings, 'bindings'),
        (Users, 'users'),
        (Groups, 'groups'),
        (ServiceAccounts, 'service_accounts'),
        (Domains, "domains"),
        (BindingsSeparationDuties, 'bindings_separation_duties')
    ]
