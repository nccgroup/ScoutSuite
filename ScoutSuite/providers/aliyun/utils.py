from aliyunsdkcore.client import AcsClient

from ScoutSuite.core.console import print_exception


def aliyun_connect_service(service, credentials, region_name=None):
    try:
        return AcsClient(credential=credentials, region_id=region_name if region_name else 'cn-hangzhou')

    except Exception as e:
        print_exception(e)
        return None
