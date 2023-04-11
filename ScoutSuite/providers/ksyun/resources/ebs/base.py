from ScoutSuite.providers.ksyun.facade.base import KsyunFacade
from ScoutSuite.providers.ksyun.resources.regions import Regions
from ScoutSuite.providers.ksyun.resources.ebs.volumes import Volumes
from ScoutSuite.providers.ksyun.resources.ebs.snapshots import Snapshots


class EBS(Regions):
    _children = [
        (Volumes, 'volumes'),
        (Snapshots, 'snapshots')
    ]

    def __init__(self, facade: KsyunFacade):
        super().__init__('ebs', facade)
