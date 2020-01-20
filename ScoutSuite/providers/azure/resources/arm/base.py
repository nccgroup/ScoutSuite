from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .role_assignments import RoleAssignments
from .roles import Roles


class ARM(Subscriptions):
    _children = [
        (Roles, 'roles'),
        (RoleAssignments, 'role_assignments')
    ]
