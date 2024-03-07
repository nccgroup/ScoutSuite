import os
from ScoutSuite.providers.do.services import DigitalOceanServicesConfig
from ScoutSuite.providers.base.provider import BaseProvider


class DigitalOceanProvider(BaseProvider):
    """
    Implements provider for DigitalOcean
    """

    def __init__(
        self,
        report_dir=None,
        timestamp=None,
        services=None,
        skipped_services=None,
        **kwargs,
    ):

        services = [] if services is None else services
        skipped_services = [] if skipped_services is None else skipped_services

        self.metadata_path = (
            "%s/metadata.json" % os.path.split(os.path.abspath(__file__))[0]
        )

        self.provider_code = "do"
        self.provider_name = "DigitalOcean"
        self.environment = "default"

        self.services_config = DigitalOceanServicesConfig

        self.credentials = kwargs["credentials"]
        self.account_id = self.credentials.client.account.get()
        self.account_id = self.account_id["account"]["uuid"]

        super().__init__(report_dir, timestamp, services, skipped_services)

    def get_report_name(self):
        """
        Returns the name of the report using the provider's configuration
        """
        if self.account_id:
            return f"do-{self.account_id}"
        else:
            return "do"

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):

        super().preprocessing()
