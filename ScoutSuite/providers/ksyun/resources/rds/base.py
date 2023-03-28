from ScoutSuite.providers.ksyun.facade.base import KsyunFacade
from ScoutSuite.providers.ksyun.resources.regions import Regions
from ScoutSuite.providers.ksyun.resources.rds.instances import Instances


class RDS(Regions):
    _children = [
        (Instances, 'instances')
    ]

    def __init__(self, facade: KsyunFacade):
        super().__init__('rds', facade)

