from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .role_assignments import RoleAssignments
from .roles import Roles


class RBAC(Subscriptions):
    _children = [
        (Roles, 'roles'),
        (RoleAssignments, 'role_assignments')
    ]
