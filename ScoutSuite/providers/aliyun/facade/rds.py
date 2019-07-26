from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest

from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.utils import get_response
from ScoutSuite.providers.aliyun.utils import get_client


class RDSFacade:
    def __init__(self, credentials: AliyunCredentials):
        self._credentials = credentials

    async def get_instances(self, region):
        """
        Get all instances

        :return: a list of all instances
        """
        client = get_client(credentials=self._credentials, region=region)
        response = await get_response(client=client,
                                      request=DescribeDBInstancesRequest.DescribeDBInstancesRequest())
        if response:
            return response['Items']['DBInstance']
        else:
            return []
