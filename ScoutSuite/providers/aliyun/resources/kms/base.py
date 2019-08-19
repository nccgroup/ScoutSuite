from ScoutSuite.providers.aliyun.resources.regions import Regions
from ScoutSuite.providers.aliyun.facade.base import AliyunFacade
from ScoutSuite.providers.aliyun.resources.kms.keys import Keys


class KMS(Regions):
    _children = [
        (Keys, 'keys')
    ]

    def __init__(self, facade: AliyunFacade):
        super(KMS, self).__init__('kms', facade)
