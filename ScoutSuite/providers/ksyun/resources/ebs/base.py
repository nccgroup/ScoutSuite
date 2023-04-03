from ScoutSuite.providers.ksyun.facade.base import KsyunFacade
from ScoutSuite.providers.ksyun.resources.regions import Regions
from ScoutSuite.providers.ksyun.resources.ebs.volumes import Volumes


class EBS(Regions):
    _children = [
        (Volumes, 'volumes')
    ]

    def __init__(self, facade: KsyunFacade):
        super().__init__('ebs', facade)
