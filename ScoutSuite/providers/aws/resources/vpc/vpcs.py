from ScoutSuite.providers.aws.resources.vpcs import Vpcs

from .network_acls import NetworkACLs
from .subnets import Subnets


class RegionalVpcs(Vpcs):
    _children = [
        (NetworkACLs, 'network_acls'),
        (Subnets, 'subnets'),
    ]

    def __init__(self, facade, scope: dict):
        super(RegionalVpcs, self).__init__(facade, scope, add_ec2_classic=True)
