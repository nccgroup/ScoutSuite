import os
from ScoutSuite.providers.openstack.services import OpenstackServicesConfig
from ScoutSuite.providers.base.provider import BaseProvider


class OpenstackProvider(BaseProvider):
    """
    Implements provider for Openstack
    """

    def __init__(self, report_dir=None, timestamp=None, services=None, skipped_services=None, **kwargs):

        services = [] if services is None else services
        skipped_services = [] if skipped_services is None else skipped_services

        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]

        self.provider_code = 'openstack'
        self.provider_name = 'Openstack'
        self.environment = None
        self.credentials = kwargs['credentials']

        self.account_id = self.credentials.session.current_user_id
        self.services_config = OpenstackServicesConfig

        super(OpenstackProvider, self).__init__(report_dir, timestamp, services, skipped_services)

    def get_report_name(self):
        """
        Returns the name of the report using the provider's configuration
        """
        if self.account_id:
            return 'openstack-{}'.format(self.account_id)
        else:
            return 'openstack'

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):

        super(OpenstackProvider, self).preprocessing()
