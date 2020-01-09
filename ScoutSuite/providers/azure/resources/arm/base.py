from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .roles import Roles
from .role_assignments import RoleAssignments


class ARM(Subscriptions):
    _children = [
        (Roles, 'roles'),
        (RoleAssignments, 'role_assignments')

    ]


