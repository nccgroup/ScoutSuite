from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials

from ScoutSuite.providers.aliyun.utils import get_oss_client


class OSSFacade:
    def __init__(self, credentials: AliyunCredentials):
        self._credentials = credentials

    async def get_buckets(self):
        """
        Get all instances

        :return: a list of all instances
        """
        client = get_oss_client(credentials=self._credentials)
        response = client.list_buckets()  # TODO this doesn't follow standards
        if response:
            return response.buckets
        else:
            return []
