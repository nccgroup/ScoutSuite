from ScoutSuite.providers.aliyun.resources.regions import Regions
from ScoutSuite.providers.aliyun.resources.vpc.vpcs import VPCs
from ScoutSuite.providers.aliyun.facade.base import AliyunFacade


class VPC(Regions):
    _children = [
        (VPCs, 'vpcs')
    ]

    def __init__(self, facade: AliyunFacade):
        super(VPC, self).__init__('vpc', facade)
