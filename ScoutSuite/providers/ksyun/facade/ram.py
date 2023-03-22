import json

from ksyun.common.common_client import CommonClient
from ksyun.common import credential
from ksyun.common.exception.ksyun_sdk_exception import KsyunSDKException
from ksyun.common.profile.client_profile import ClientProfile
from ksyun.common.profile.http_profile import HttpProfile

from ScoutSuite.providers.ksyun.authentication_strategy import KsyunCredentials


class RAMFacade():
    def __init__(self, credentials: KsyunCredentials):
        self._credentials = credentials

    async def get_users(self):
        """
        Get all users

        :return: a list of all users
        """
        # response = await get_response(client=self._client, request=ListUsersRequest.ListUsersRequest())
        try:
            cred = credential.Credential(self._credentials.credentials_id, self._credentials.credentials_secret)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "iam.api.ksyun.com"
            httpProfile.reqMethod = "POST"
            httpProfile.reqTimeout = 60
            httpProfile.scheme = "http"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile

            common_client = CommonClient("iam", '2015-11-01', cred, "cn-beijing-6", profile=clientProfile)
            r = common_client.call("ListUsers", {})
            response = json.loads(r).get('ListUserResult')
            if response:
                return response['member']
            else:
                return []
        except KsyunSDKException as err:
            print(err)

    async def get_user_details(self, username):
        """
        Get additional details for a user

        :param username: The username of the user
        :return: a dict with the user's details
        """
        try:
            cred = credential.Credential(self._credentials.credentials_id, self._credentials.credentials_secret)

            httpProfile = HttpProfile()
            httpProfile.endpoint = "iam.api.ksyun.com"
            httpProfile.reqMethod = "POST"
            httpProfile.reqTimeout = 60
            httpProfile.scheme = "http"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile

            common_client = CommonClient("iam", '2015-11-01', cred, "cn-beijing-6", profile=clientProfile)
            r = common_client.call("GetUser", {"UserName": username})
            response = json.loads(r).get("GetUserResult")
            if response:
                return response['User']
            else:
                return []
        except KsyunSDKException as err:
            print(err)
