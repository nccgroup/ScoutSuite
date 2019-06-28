from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest

from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.utils import get_response


class RDSFacade:
    def __init__(self, credentials: AliyunCredentials):
        self._client = credentials.client

    async def get_instances(self):
        """
        Get all instances

        :return: a list of all instances
        """
        response = await get_response(client=self._client,
                                      request=DescribeDBInstancesRequest.DescribeDBInstancesRequest())
        return response['Items']['DBInstance']
