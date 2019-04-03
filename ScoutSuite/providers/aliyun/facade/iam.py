import asyncio
import functools
import json


from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials

from aliyunsdkram.request.v20150501 import ListUsersRequest, ListAccessKeysRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException

from ScoutSuite.providers.utils import run_concurrently


class IAMFacade:

    def __init__(self, credentials: AliyunCredentials):
        self._client = credentials.client

    async def get_users(self):

        # TODO handle truncated response
        try:
            response = await run_concurrently(lambda:
                                          self._client.do_action_with_exception(ListUsersRequest.ListUsersRequest()))
            response_decoded = json.loads(response)
            return response_decoded['Users']['User']
        except ServerException as e:
            print(e)  # TODO log
        except ClientException as e:
            print(e)  # TODO log

    async def get_user_api_keys(self, username):

        # TODO handle truncated response
        try:

            request = ListAccessKeysRequest.ListAccessKeysRequest()
            request.set_UserName(username)
            response = await run_concurrently(lambda:
                                              self._client.do_action_with_exception(request))
            response_decoded = json.loads(response)
            return response_decoded['AccessKeys']['AccessKey']
        except ServerException as e:
            print(e)  # TODO log
        except ClientException as e:
            print(e)  # TODO log
