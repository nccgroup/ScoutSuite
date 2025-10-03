import oss2
import asyncio
from asyncio_throttle import Throttler
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider

from ScoutSuite.core.console import print_exception


def _ensure_throttler():
    """
    Attach a Throttler to the current running event loop if not already present.
    Falls back to the default event loop if no running loop is set.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        try:
            loop = asyncio.get_event_loop()
        except Exception:
            return
    if not hasattr(loop, 'throttler'):
        # Conservative default: 10 requests per second
        try:
            loop.throttler = Throttler(rate_limit=10, period=1)
        except Exception:
            # Do not fail provider initialization if throttler cannot be created
            pass


def _configure_endpoints(region):
    try:
        if not region:
            return
        # Register product endpoints explicitly to avoid resolver issues
        region_provider.add_endpoint('Ecs', region, f'ecs.{region}.aliyuncs.com')
        region_provider.add_endpoint('Vpc', region, f'vpc.{region}.aliyuncs.com')
        region_provider.add_endpoint('Rds', region, f'rds.{region}.aliyuncs.com')
        region_provider.add_endpoint('Kms', region, f'kms.{region}.aliyuncs.com')
        region_provider.add_endpoint('Sts', region, 'sts.aliyuncs.com')
        region_provider.add_endpoint('Ram', region, 'ram.aliyuncs.com')
        region_provider.add_endpoint('Actiontrail', region, f'actiontrail.{region}.aliyuncs.com')
        region_provider.add_endpoint('Ocs', region, f'ocs.{region}.aliyuncs.com')
    except Exception:
        # Ignore endpoint registration failures; SDK may still resolve defaults
        pass


def get_client(credentials, region=None):
    try:
        _ensure_throttler()
        region_to_use = region if region else 'cn-hangzhou'
        _configure_endpoints(region_to_use)
        client = AcsClient(credential=credentials.credentials, region_id=region_to_use)
        try:
            client.set_connect_timeout(10)
            client.set_read_timeout(20)
        except Exception:
            pass
        return client

    except Exception as e:
        print_exception(e)
        return None


def get_oss_client(credentials, region=None):
    try:
        _ensure_throttler()
        auth = oss2.Auth(credentials.credentials.access_key_id, credentials.credentials.access_key_secret)
        client = oss2.Service(auth,
                              endpoint=f'oss-{region}.aliyuncs.com' if region
                              else 'oss-cn-hangzhou.aliyuncs.com')
        return client

    except Exception as e:
        print_exception(e)
        return None
