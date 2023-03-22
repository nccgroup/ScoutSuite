import json

from ScoutSuite.providers.ksyun.authentication_strategy import KsyunCredentials
from ScoutSuite.providers.ksyun.utils import ksc_open_api
from ksyun.common.common_client import CommonClient
from ksyun.common import credential
from ksyun.common.exception.ksyun_sdk_exception import KsyunSDKException
from ksyun.common.profile.client_profile import ClientProfile
from ksyun.common.profile.http_profile import HttpProfile


class KECFacade:
    def __init__(self, credentials: KsyunCredentials):
        self._credentials = credentials

    async def get_instances(self, region):
        """
        Get all instances

        :return: a list of all instances
        """
        # try:
        #     r = ksc_open_api(self._credentials.credentials_id, self._credentials.credentials_secret, 'kec', 'DescribeInstances', region)
        #     response = json.loads(r).get('InstancesSet')
        #     if response:
        #         return response
        #     else:
        #         return []
        # except KsyunSDKException as err:
        #     print(err)
        try:
            cred = credential.Credential(self._credentials.credentials_id, self._credentials.credentials_secret)

            httpProfile = HttpProfile()
            httpProfile.endpoint = "kec.api.ksyun.com"
            httpProfile.reqMethod = "POST"
            httpProfile.reqTimeout = 60
            httpProfile.scheme = "http"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile

            common_client = CommonClient("kec", '2016-03-04', cred, region=region, profile=clientProfile)
            r = common_client.call("DescribeInstances", {})
            response = json.loads(r).get('InstancesSet')
            if response:
                return response
            else:
                return []
        except KsyunSDKException as err:
            print(err)


        
        



