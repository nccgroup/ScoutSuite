from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.ram import RAMFacade
from ScoutSuite.providers.aliyun.facade.actiontrail import ActiontrailFacade


class AliyunFacade():
    def __init__(self, credentials: AliyunCredentials):
        self.ram = RAMFacade(credentials)
        self.actiontrail = ActiontrailFacade(credentials)
