from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .role_assignments import RoleAssignments
from .roles import Roles
from .custom_roles_report import  CustomRolesReport


class RBAC(Subscriptions):
    _children = [
        (Roles, 'roles'),
        (RoleAssignments, 'role_assignments'),
        (CustomRolesReport, 'custom_roles_report'),
    ]

    def get_user_id_list(self):
        """
        Generates and returns a unique list of user IDs which have a role assigned.
        """
        user_set = set()
        for subscription in self['subscriptions'].values():
            for role_assignment in subscription['role_assignments'].values():
                if role_assignment['principal_type'] == 'User':
                    user_set.add(role_assignment['principal_id'])
        return list(user_set)

