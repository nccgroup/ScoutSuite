from aliyunsdkkms.request.v20160120 import ListKeysRequest, DescribeKeyRequest
from ScoutSuite.providers.aliyun.utils import get_client

from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.utils import get_response


class KMSFacade:
    def __init__(self, credentials: AliyunCredentials):
        self._credentials = credentials

    async def get_keys(self, region):
        """
        Get all keys

        :return: a list of all keys
        """
        client = get_client(credentials=self._credentials, region=region)
        response = await get_response(client=client,
                                      request=ListKeysRequest.ListKeysRequest())
        if response:
            return response['Keys']['Key']
        else:
            return []

    async def get_key_details(self, key_id, region):
        """
        Gets details for a key

        :return: a dictionary of details
        """
        client = get_client(credentials=self._credentials, region=region)
        request = DescribeKeyRequest.DescribeKeyRequest()
        request.set_KeyId(key_id)
        response = await get_response(client=client,
                                      request=request)
        if response:
            return response['KeyMetadata']
        else:
            return []
