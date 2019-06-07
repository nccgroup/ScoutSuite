import os

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

        super(AliyunProvider, self).__init__(report_dir, timestamp, services, skipped_services)

    def get_report_name(self):
        """
        Returns the name of the report using the provider's configuration
        """
        if self.account_id:
            return 'aliyun-{}'.format(self.account_id)
        else:
            return 'aliyun'

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):

        super(AliyunProvider, self).preprocessing()

