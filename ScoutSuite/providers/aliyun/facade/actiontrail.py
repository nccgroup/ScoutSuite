from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.utils import get_response

from aliyunsdkactiontrail.request.v20171204 import DescribeTrailsRequest

from ScoutSuite.providers.aliyun.utils import get_client


class ActiontrailFacade:
    def __init__(self, credentials: AliyunCredentials):
        self._credentials = credentials
        self._client = get_client(credentials=self._credentials)

    async def get_trails(self):
        """
        Get all users

        :return: a list of all users
        """
        response = await get_response(client=self._client,
                                      request=DescribeTrailsRequest.DescribeTrailsRequest())
        if response:
            return response['TrailList']
        else:
            return []
