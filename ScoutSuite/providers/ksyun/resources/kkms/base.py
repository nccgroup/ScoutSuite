from ScoutSuite.providers.ksyun.resources.regions import Regions
from ScoutSuite.providers.ksyun.facade.base import KsyunFacade
from ScoutSuite.providers.ksyun.resources.kkms.keys import Keys


class KKMS(Regions):
    _children = [
        (Keys, 'keys')
    ]

    def __init__(self, facade: KsyunFacade):
        super().__init__('kkms', facade)
