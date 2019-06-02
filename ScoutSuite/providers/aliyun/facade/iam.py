from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.utils import get_response

from aliyunsdkram.request.v20150501 import ListUsersRequest, ListAccessKeysRequest


class IAMFacade:
    def __init__(self, credentials: AliyunCredentials):
        self._client = credentials.client

    async def get_users(self):
        """
        Get all users

        :return: a list of all users
        """
        response = await get_response(client=self._client,
                                request=ListUsersRequest.ListUsersRequest())
        return response['Users']['User']

    async def get_user_api_keys(self, username):
        """
        Get API keys for a user

        :param username: The username of the user
        :return: the list of API keys for that user
        """
        request = ListAccessKeysRequest.ListAccessKeysRequest()
        request.set_UserName(username)
        response = await get_response(client=self._client,
                                      request=request)
        return response['AccessKeys']['AccessKey']
