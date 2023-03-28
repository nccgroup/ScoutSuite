from ScoutSuite.providers.ksyun.resources.regions import Regions
from ScoutSuite.providers.ksyun.resources.vpc.vpcs import VPCs
from ScoutSuite.providers.ksyun.facade.base import KsyunFacade


class VPC(Regions):
    _children = [
        (VPCs, 'vpcs')
    ]

    def __init__(self, facade: KsyunFacade):
        super().__init__('vpc', facade)
