import os

from ScoutSuite.providers.oci.services import OracleServicesConfig
from ScoutSuite.providers.base.provider import BaseProvider


class OracleProvider(BaseProvider):
    """
    Implements provider for Azure
    """

    def __init__(self,
                 report_dir=None, timestamp=None, services=None, skipped_services=None, **kwargs):

        services = [] if services is None else services
        skipped_services = [] if skipped_services is None else skipped_services

        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]

        self.provider_code = 'oci'
        self.provider_name = 'Oracle Cloud Infrastructure'
        self.environment = 'default'

        self.services_config = OracleServicesConfig

        self.credentials = kwargs['credentials']
        self.account_id = self.credentials.get_scope()

        super().__init__(report_dir, timestamp, services, skipped_services)

    def get_report_name(self):
        """
        Returns the name of the report using the provider's configuration
        """
        if self.account_id:
            return f'oracle-{self.account_id}'
        else:
            return 'oracle'

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):

        super().preprocessing()

