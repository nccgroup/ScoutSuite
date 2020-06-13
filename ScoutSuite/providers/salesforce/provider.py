import os
from ScoutSuite.providers.salesforce.services import SalesforceServicesConfig
from ScoutSuite.providers.base.provider import BaseProvider


class SalesforceProvider(BaseProvider):
    """
    Implements provider for Salesforce
    """

    def __init__(self, report_dir=None, timestamp=None, services=None, skipped_services=None, **kwargs):

        services = [] if services is None else services
        skipped_services = [] if skipped_services is None else skipped_services

        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]

        self.provider_code = 'salesforce'
        self.provider_name = 'Salesforce'
        self.environment = None
        self.credentials = kwargs['credentials']
        self.account_id = self.credentials.username

        self.services_config = SalesforceServicesConfig

        super(SalesforceProvider, self).__init__(report_dir, timestamp, services, skipped_services)

    def get_report_name(self):
        """
        Returns the name of the report using the provider's configuration
        """
        if self.credentials:
            return 'salesforce-{}'.format(self.credentials.username.split('@')[0])
        else:
            return 'salesforce'

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):

        super(SalesforceProvider, self).preprocessing()