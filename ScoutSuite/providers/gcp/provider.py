# -*- coding: utf-8 -*-

import os

from ScoutSuite.providers.base.provider import BaseProvider


class GCPProvider(BaseProvider):
    """
    Implements provider for AWS
    """

    def __init__(self, profile, report_dir=None, timestamp=None, services=[], skipped_services=[], thread_config=4):

        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]

        self.profile = profile
        self.aws_account_id = None

        super(GCPProvider, self).__init__(report_dir, timestamp, services, skipped_services, thread_config)

    def authenticate(self, profile, csv_credentials, mfa_serial, mfa_code):
        """
        Implement authentication for the AWS provider
        :return:
        """
        self.credentials = '1'  # TODO implement this

        self.aws_account_id = get_aws_account_id(self.credentials)

    def preprocessing(self, ip_ranges=[], ip_ranges_name_key=None):
        """
        TODO description
        Tweak the AWS config to match cross-service resources and clean any fetching artifacts

        :param ip_ranges:
        :param ip_ranges_name_key:
        :return: None
        """

        super(GCPProvider, self).preprocessing()
