from ScoutSuite.providers.aws.resources.regions import Regions

from .vpcs import ELBv2Vpcs


class ELBv2(Regions):
    _children = [
        (ELBv2Vpcs, 'vpcs')
    ]

    def __init__(self):
        super(ELBv2, self).__init__('elbv2')
