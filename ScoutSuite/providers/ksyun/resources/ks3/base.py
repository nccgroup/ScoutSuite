from ScoutSuite.providers.ksyun.facade.base import KsyunFacade
from ScoutSuite.providers.ksyun.resources.regions import Regions
from ScoutSuite.providers.ksyun.resources.ks3.buckets import Buckets


class KS3(Regions):
    _children = [
        (Buckets, 'buckets')
    ]

    def __init__(self, facade: KsyunFacade):
        super().__init__('kec', facade)
