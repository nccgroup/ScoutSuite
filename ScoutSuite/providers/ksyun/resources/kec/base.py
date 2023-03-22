from ScoutSuite.providers.ksyun.facade.base import KsyunFacade
from ScoutSuite.providers.ksyun.resources.regions import Regions
from ScoutSuite.providers.ksyun.resources.kec.instances import Instances


class KEC(Regions):
    _children = [
        (Instances, 'instances')
    ]

    def __init__(self, facade: KsyunFacade):
        super().__init__('kec', facade)
