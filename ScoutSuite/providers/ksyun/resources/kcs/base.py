from ScoutSuite.providers.ksyun.facade.base import KsyunFacade
from ScoutSuite.providers.ksyun.resources.regions import Regions
from ScoutSuite.providers.ksyun.resources.kcs.clusters import Clusters


class KCS(Regions):
    _children = [
        (Clusters, 'clusters')
    ]

    def __init__(self, facade: KsyunFacade):
        super().__init__('kcs', facade)
