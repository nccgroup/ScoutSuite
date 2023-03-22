import json
from ksyun.common.common_client import CommonClient
from ksyun.common import credential
from ksyun.common.exception.ksyun_sdk_exception import KsyunSDKException
from ksyun.common.profile.client_profile import ClientProfile
from ksyun.common.profile.http_profile import HttpProfile

from ScoutSuite.providers.ksyun.authentication_strategy import KsyunCredentials


class ActiontrailFacade:
    def __init__(self, credentials: KsyunCredentials):
        self._credentials = credentials

    async def get_trails(self):
        """
        Get all users

        :return: a list of all users
        """
        try:
            cred = credential.Credential(self._credentials.credentials_id, self._credentials.credentials_secret)

            httpProfile = HttpProfile()
            httpProfile.endpoint = "actiontrail.api.ksyun.com"
            httpProfile.reqMethod = "GET"
            httpProfile.reqTimeout = 60
            httpProfile.scheme = "http"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile

            common_client = CommonClient("actiontrail", '2019-04-01', cred, "cn-beijing-6", profile=clientProfile)
            r = common_client.call("ListOperateLogs", {"PageSize": "20"})
            response = json.loads(r).get('Events')
            if response:
                return response
            else:
                return []
        except KsyunSDKException as err:
            print(err)
        # response = []
