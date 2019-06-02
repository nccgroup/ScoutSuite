from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.iam import IAMFacade
from ScoutSuite.providers.aliyun.facade.actiontrail import ActiontrailFacade


class AliyunFacade():
    def __init__(self, credentials: AliyunCredentials):
        self.iam = IAMFacade(credentials)
        self.actiontrail = ActiontrailFacade(credentials)
