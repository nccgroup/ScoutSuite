from aliyunsdkkms.request.v20160120 import ListKeysRequest

from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.utils import get_response


class KMSFacade:
    def __init__(self, credentials: AliyunCredentials):
        self._client = credentials.client

    async def get_keys(self):
        """
        Get all keys

        :return: a list of all keys
        """

        self._client.set_region_id('eu-west-1')  # FIXME this shouldn't be done here

        response = await get_response(client=self._client,
                                      request=ListKeysRequest.ListKeysRequest())
        return response['Keys']['Key']
