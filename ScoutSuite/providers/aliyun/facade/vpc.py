from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.utils import get_response

from ScoutSuite.core.console import print_exception
from aliyunsdkvpc.request.v20160428 import DescribeVpcsRequest


class VPCFacade:
    def __init__(self, credentials: AliyunCredentials):
        self._client = credentials.client

    async def get_vpcs(self):
        """
        Get all VPCs

        :return: a list of all VPCs
        """
        response = await get_response(client=self._client,
                                      request=DescribeVpcsRequest.DescribeVpcsRequest())
        return response['Vpcs']
