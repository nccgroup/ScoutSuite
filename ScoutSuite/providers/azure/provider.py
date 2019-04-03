import os

from ScoutSuite.providers.azure.services import AzureServicesConfig
from ScoutSuite.providers.base.provider import BaseProvider
from ScoutSuite.providers.azure.services import AzureServicesConfig


class AzureProvider(BaseProvider):
    """
    Implements provider for Azure
    """

    def __init__(self, project_id=None, organization_id=None,
                 report_dir=None, timestamp=None, services=None, skipped_services=None, thread_config=4, **kwargs):
        services = [] if services is None else services
        skipped_services = [] if skipped_services is None else skipped_services

        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]

        self.provider_code = 'azure'
        self.provider_name = 'Microsoft Azure'
        self.environment = 'default'

        self.services_config = AzureServicesConfig

        self.credentials = kwargs['credentials']
        self.account_id = self.credentials.subscription_id

        super(AzureProvider, self).__init__(report_dir, timestamp,
                                            services, skipped_services, thread_config)

    def get_report_name(self):
        """
        Returns the name of the report using the provider's configuration
        """
        if self.credentials.subscription_id:
            return 'azure-{}'.format(self.credentials.subscription_id)
        else:
            return 'azure'

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):
        """
        TODO description
        Tweak the AWS config to match cross-service resources and clean any fetching artifacts

        :param ip_ranges:
        :param ip_ranges_name_key:
        :return: None
        """
        ip_ranges = [] if ip_ranges is None else ip_ranges
        super(AzureProvider, self).preprocessing()
