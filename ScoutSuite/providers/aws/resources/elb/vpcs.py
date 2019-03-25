from ScoutSuite.providers.aws.resources.vpcs import Vpcs
from .load_balancers import LoadBalancers


class ELBVpcs(Vpcs):
    _children = [
        (LoadBalancers, 'elbs'),
    ]

    def __init__(self, facade, scope: dict):
        super(ELBVpcs, self).__init__(facade, scope, add_ec2_classic=True)
