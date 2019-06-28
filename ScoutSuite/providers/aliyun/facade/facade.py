from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.ram import RAMFacade
from ScoutSuite.providers.aliyun.facade.ecs import ECSFacade
from ScoutSuite.providers.aliyun.facade.rds import RDSFacade
from ScoutSuite.providers.aliyun.facade.vpc import VPCFacade
from ScoutSuite.providers.aliyun.facade.actiontrail import ActiontrailFacade


class AliyunFacade():
    def __init__(self, credentials: AliyunCredentials):
        self.actiontrail = ActiontrailFacade(credentials)
        self.ram = RAMFacade(credentials)
        self.ecs = ECSFacade(credentials)
        self.rds = RDSFacade(credentials)
        self.vpc = VPCFacade(credentials)
