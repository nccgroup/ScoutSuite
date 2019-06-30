from aliyunsdkcore.client import AcsClient

from ScoutSuite.core.console import print_exception


def get_client(credentials, region=None):
    try:
        return AcsClient(credential=credentials,
                         region_id=region if region else 'cn-hangzhou')

    except Exception as e:
        print_exception(e)
        return None
