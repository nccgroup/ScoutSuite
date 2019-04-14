from ScoutSuite.providers.aws.resources.vpcs import Vpcs

from .network_acls import NetworkACLs
from .subnets import Subnets


class RegionalVpcs(Vpcs):
    _children = [
        (NetworkACLs, 'network_acls'),
        (Subnets, 'subnets'),
    ]
