from aliyunsdkcore.client import AcsClient
from aliyunsdksts.request.v20150401 import GetCallerIdentityRequest
import json

from ScoutSuite.core.console import print_exception


def get_client(credentials, region=None):
    try:
        client = AcsClient(credential=credentials.credentials, region_id=region if region else 'cn-hangzhou')
        return client

    except Exception as e:
        print_exception(e)
        return None
