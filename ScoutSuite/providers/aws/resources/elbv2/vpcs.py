from ScoutSuite.providers.aws.resources.vpcs import Vpcs
from .load_balancers import LoadBalancers


class ELBv2Vpcs(Vpcs):
    _children = [
        (LoadBalancers, 'lbs'),
    ]

    def __init__(self, facade, scope: dict):
        super(ELBv2Vpcs, self).__init__(facade, scope, add_ec2_classic=True)
