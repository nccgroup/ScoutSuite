import os
import asyncio
import warnings
from asyncio_throttle import Throttler

try:
    from urllib3.exceptions import SNIMissingWarning
except Exception:
    SNIMissingWarning = None

# Suppress vendored urllib3 SNI false-positive warnings
warnings.filterwarnings('ignore', message='An HTTPS request has been made, but the SNI (Server Name Indication) extension to TLS is not available on this platform.*')
if SNIMissingWarning:
    warnings.filterwarnings('ignore', category=SNIMissingWarning)

from ScoutSuite.providers.aliyun.services import AliyunServicesConfig
from ScoutSuite.providers.base.provider import BaseProvider


class AliyunProvider(BaseProvider):
    """
    Implements provider for Azure
    """

    def __init__(self,
                 report_dir=None, timestamp=None, services=None, skipped_services=None, **kwargs):

        services = [] if services is None else services
        skipped_services = [] if skipped_services is None else skipped_services

        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]

        self.provider_code = 'aliyun'
        self.provider_name = 'Alibaba Cloud'
        self.environment = 'default'

        self.services_config = AliyunServicesConfig

        self.credentials = kwargs['credentials']
        self.account_id = self.credentials.caller_details['AccountId']

        # Ensure throttler is available on the event loop as early as possible
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        if not hasattr(loop, 'throttler'):
            loop.throttler = Throttler(rate_limit=10, period=1)

        super().__init__(report_dir, timestamp, services, skipped_services)

    def get_report_name(self):
        """
        Returns the name of the report using the provider's configuration
        """
        if self.account_id:
            return f'aliyun-{self.account_id}'
        else:
            return 'aliyun'

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):
        # Ensure a global throttler is attached to the event loop for concurrency control
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop = asyncio.get_event_loop()
        if not hasattr(loop, 'throttler'):
            loop.throttler = Throttler(rate_limit=10, period=1)

        super().preprocessing()

