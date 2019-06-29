from aliyunsdkcore.client import AcsClient

from ScoutSuite.core.console import print_exception


def get_client(credentials, region_name=None):
    try:
        return AcsClient(credential=credentials,
                         region_id=region_name if region_name else 'cn-hangzhou')

    except Exception as e:
        print_exception(e)
        return None
