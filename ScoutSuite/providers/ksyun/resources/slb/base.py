from ScoutSuite.providers.ksyun.facade.base import KsyunFacade
from ScoutSuite.providers.ksyun.resources.regions import Regions
from ScoutSuite.providers.ksyun.resources.slb.listeners import Listeners


class SLB(Regions):
    _children = [
        (Listeners, 'listeners')
    ]

    def __init__(self, facade: KsyunFacade):
        super().__init__('slb', facade)
