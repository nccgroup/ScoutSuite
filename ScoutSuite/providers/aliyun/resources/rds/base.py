from ScoutSuite.providers.aliyun.facade.base import AliyunFacade
from ScoutSuite.providers.aliyun.resources.regions import Regions
from ScoutSuite.providers.aliyun.resources.rds.instances import Instances


class RDS(Regions):
    _children = [
        (Instances, 'instances')
    ]

    def __init__(self, facade: AliyunFacade):
        super().__init__('rds', facade)
