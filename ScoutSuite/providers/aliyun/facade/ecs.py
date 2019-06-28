from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest

from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.utils import get_response


class ECSFacade:
    def __init__(self, credentials: AliyunCredentials):
        self._client = credentials.client
        # self._client.set_region_id('eu-west-1')  # FIXME this shouldn't be done here

    async def get_instances(self):
        """
        Get all instances

        :return: a list of all instances
        """
        response = await get_response(client=self._client,
                                      request=DescribeInstancesRequest.DescribeInstancesRequest())
        return response['Instances']['Instance']
