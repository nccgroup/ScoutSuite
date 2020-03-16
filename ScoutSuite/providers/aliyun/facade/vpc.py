from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.utils import get_response
from ScoutSuite.providers.aliyun.utils import get_client

from aliyunsdkvpc.request.v20160428 import DescribeVpcsRequest


class VPCFacade:
    def __init__(self, credentials: AliyunCredentials):
        self._credentials = credentials

    async def get_vpcs(self, region):
        """
        Get all VPCs

        :return: a list of all VPCs
        """
        client = get_client(credentials=self._credentials, region=region)
        response = await get_response(client=client,
                                      request=DescribeVpcsRequest.DescribeVpcsRequest())
        if response:
            return response['Vpcs']['Vpc']
        else:
            return []
