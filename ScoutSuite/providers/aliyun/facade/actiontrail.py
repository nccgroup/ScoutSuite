from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.utils import get_response

from aliyunsdkactiontrail.request.v20171204 import DescribeTrailsRequest


class ActiontrailFacade:
    def __init__(self, credentials: AliyunCredentials):
        self._client = credentials.client

    async def get_trails(self):
        """
        Get all users

        :return: a list of all users
        """
        response = await get_response(client=self._client,
                                      request=DescribeTrailsRequest.DescribeTrailsRequest())
        return response['TrailList']
