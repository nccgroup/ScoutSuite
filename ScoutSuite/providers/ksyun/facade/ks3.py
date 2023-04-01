import json

import requests
from ksyun.common.common_client import CommonClient
from ksyun.common import credential
from ksyun.common.exception.ksyun_sdk_exception import KsyunSDKException
from ksyun.common.profile.client_profile import ClientProfile
from ksyun.common.profile.http_profile import HttpProfile

from ScoutSuite.providers.ksyun.authentication_strategy import KsyunCredentials


class KS3Facade:
    def __init__(self, credentials: KsyunCredentials):
        self._credentials = credentials

    async def get_buckets(self):
        url = "https://ks3.console.ksyun.com/i/ks3/ks3-www/api/?projectIds=0,106536"
        headers = {
            "Accept": "application/json",
            "Cookie": "kscdigest=77372c6d8a01ef3b46dca11e3ef3f1dc-1344489989;"
        }
        try:
            r = requests.get(url, headers=headers)
            response = json.loads(r.text).get("bucketListV2")
            if response:
                return response
            else:
                return []
        except KsyunSDKException as err:
            return []
