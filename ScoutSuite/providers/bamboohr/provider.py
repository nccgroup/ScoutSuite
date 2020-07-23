from __future__ import print_function
from __future__ import unicode_literals

import copy
import json

from ScoutSuite import __version__ as scout_version
from ScoutSuite.core.console import print_exception, print_info, print_error
from ScoutSuite.output.html import ScoutReport
from ScoutSuite.providers.base.configs.browser import get_object_at
from ScoutSuite.providers.base.provider import BaseProvider
from ScoutSuite.providers.bamboohr.services import BambooHRServicesConfig

class BambooHRProvider(BaseProvider):
    """
    Base class for the different providers.

    Root object that holds all of the necessary provider-specific resources and Scout configuration items.

    For each supported cloud provider, a child class will be created which implements the necessary code.
    In addition, each method of children classes will call the base provider in order to execute code required for
    all cloud providers
    """

    def __init__(self, report_dir=None, timestamp=None,
                 services=None, skipped_services=None,
                 result_format='json', **kwargs):
        """

        :account_id         account ID
        :last_run           Information about the last run
        :metadata           Metadata used to generate the HTML report
        :ruleset            Ruleset used to perform the analysis
        :services           AWS configuration sorted by service
        """
        services = [] if services is None else services
        skipped_services = [] if skipped_services is None else skipped_services

        self.last_run = None
        self.metadata = None
        self.credentials = kwargs['credentials']
        self.provider_code = 'bamboohr'
        self.provider_name = 'BambooHR'
        self.environment = None
        self.account_id = None
        self.services_config = BambooHRServicesConfig

        super(BambooHRProvider, self).__init__(report_dir, timestamp, services, skipped_services)

    def get_report_name(self):
        """
        Returns the name of the report using the provider's configuration
        """
        return 'bamboohr'

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):
        """
        Used for adding cross-services configs.
        """
        # Preprocessing dictated by metadata

    def postprocessing(self, current_time, ruleset, run_parameters):
        """
        Sets post-run information.
        """
        self._update_last_run(current_time, ruleset, run_parameters)

    def _load_metadata(self):
        """
        Load the metadata as defined in the child class metadata_path attribute

        :return: None
        """
