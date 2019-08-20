from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from ScoutSuite.providers.aliyun.utils import get_client

from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.utils import get_response


class ECSFacade:
    def __init__(self, credentials: AliyunCredentials):
        self._credentials = credentials

    async def get_instances(self, region):
        """
        Get all instances

        :return: a list of all instances
        """
        client = get_client(credentials=self._credentials, region=region)
        response = await get_response(client=client,
                                      request=DescribeInstancesRequest.DescribeInstancesRequest())
        if response:
            return response['Instances']['Instance']
        else:
            return []
