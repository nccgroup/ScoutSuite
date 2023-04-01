import json

from ksyun.common.common_client import CommonClient
from ksyun.common import credential
from ksyun.common.exception.ksyun_sdk_exception import KsyunSDKException
from ksyun.common.profile.client_profile import ClientProfile
from ksyun.common.profile.http_profile import HttpProfile

from ScoutSuite.providers.ksyun.authentication_strategy import KsyunCredentials


class KS3Facade:
    def __init__(self, credentials: KsyunCredentials):
        self._credentials = credentials

    async def get_buckets(self, region):
        try:

            response = ''
            if response:
                return response
            else:
                return []
        except KsyunSDKException as err:
            return []
