import oss2
from aliyunsdkcore.client import AcsClient

from ScoutSuite.core.console import print_exception


def get_client(credentials, region=None):
    try:
        client = AcsClient(credential=credentials.credentials, region_id=region if region else 'cn-hangzhou')
        return client

    except Exception as e:
        print_exception(e)
        return None


def get_oss_client(credentials, region=None):
    try:
        auth = oss2.Auth(credentials.credentials.access_key_id, credentials.credentials.access_key_secret)
        client = oss2.Service(auth,
                              endpoint=f'oss-{region}.aliyuncs.com' if region
                              else 'oss-cn-hangzhou.aliyuncs.com')
        return client

    except Exception as e:
        print_exception(e)
        return None
