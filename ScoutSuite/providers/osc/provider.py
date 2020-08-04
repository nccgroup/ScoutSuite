import os

from ScoutSuite.providers.base.provider import BaseProvider
from ScoutSuite.providers.osc.services import OSCServicesConfig
#from ScoutSuite.providers.osc.utils import get_partition_name


class OutscaleProvider(BaseProvider):
    """
        Implements provider for Outscale
    """

    def __init__(self, profile='default', report_dir=None, timestamp=None,
        services=None, skipped_services=None, result_format='json', **kwargs):
        services = [] if services is None else services
        skipped_services = [] if skipped_services is None else skipped_services

        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]

        self.sg_map = {}
        self.subnet_map = {}

        self.profile = profile
        self.services_config = OSCServicesConfig

        self.provider_code = 'osc'
        self.provider_name = 'Outscale API'
        self.environment = self.profile
        self.result_format = result_format

        self.credentials = kwargs['credentials']
        self.account_id = ""
        super(OutscaleProvider, self).__init__(report_dir, timestamp,
                                          services, skipped_services,
                                          result_format)
